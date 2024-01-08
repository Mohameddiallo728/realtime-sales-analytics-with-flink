import models.Order;
import models.SalesPerCategory;
import models.SalesPerDay;
import models.SalesPerMonth;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
import org.apache.flink.connector.jdbc.JdbcExecutionOptions;
import org.apache.flink.connector.jdbc.JdbcSink;
import org.apache.flink.connector.jdbc.JdbcStatementBuilder;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import utils.JSONDeserializer;

import java.sql.Date;

/**
 * Created by mohamed on 12/20/23  at 4:27 PM
 **/

public class DataStreamJob {
    private static final String jdbcUrl = "jdbc:postgresql://localhost:5432/ecom_db";
    private static final String username = "postgres";
    private static final String password = "mohamed";

    public static void main(String[] args) throws Exception {
        // Sets up the execution environment, which is the main entry point
        // to building Flink applications.
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        String topic = "product_sold";

        KafkaSource<Order> source = KafkaSource.<Order>builder()
                .setBootstrapServers("localhost:9092")
                .setTopics(topic)
                .setGroupId("flink-group")
                .setStartingOffsets(OffsetsInitializer.earliest())
                .setValueOnlyDeserializer(new JSONDeserializer())
                .build();

        DataStream<Order> orderStream = env.fromSource(source, WatermarkStrategy.noWatermarks(), "Kafka source");

        orderStream.print();

        JdbcExecutionOptions execOptions = new JdbcExecutionOptions.Builder()
                .withBatchSize(1000)
                .withBatchIntervalMs(200)
                .withMaxRetries(5)
                .build();

        JdbcConnectionOptions connOptions = new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
                .withUrl(jdbcUrl)
                .withDriverName("org.postgresql.Driver")
                .withUsername(username)
                .withPassword(password)
                .build();


        //create transactions table
        orderStream.addSink(JdbcSink.sink(
                "CREATE TABLE IF NOT EXISTS transactions (" +
                        "order_id VARCHAR(255) PRIMARY KEY, " +
                        "product_id VARCHAR(255), " +
                        "product_name VARCHAR(255), " +
                        "product_category VARCHAR(255), " +
                        "product_price DOUBLE PRECISION, " +
                        "product_quantity INTEGER, " +
                        "product_brand VARCHAR(255), " +
                        "total_amount DOUBLE PRECISION, " +
                        "currency VARCHAR(255), " +
                        "customer_id VARCHAR(255), " +
                        "order_date TIMESTAMP, " +
                        "payment_method VARCHAR(255) " +
                        ")",
                (JdbcStatementBuilder<Order>) (preparedStatement, order) -> {
                },
                execOptions,
                connOptions
        )).name("Create transaction Table");

        //create sales_per_category table sink
        orderStream.addSink(JdbcSink.sink(
                "CREATE TABLE IF NOT EXISTS sales_per_category (" +
                        "order_date DATE, " +
                        "category VARCHAR(255), " +
                        "total_sales DOUBLE PRECISION, " +
                        "PRIMARY KEY (order_date, category)" +
                        ")",
                (JdbcStatementBuilder<Order>) (preparedStatement, order) -> {

                },
                execOptions,
                connOptions
        )).name("Create Sales Per Category Table");

        //create sales_per_day table sink
        orderStream.addSink(JdbcSink.sink(
                "CREATE TABLE IF NOT EXISTS sales_per_day (" +
                        "order_date DATE PRIMARY KEY, " +
                        "total_sales DOUBLE PRECISION " +
                        ")",
                (JdbcStatementBuilder<Order>) (preparedStatement, order) -> {

                },
                execOptions,
                connOptions
        )).name("Create Sales Per Day Table");

        //create sales_per_month table sink
        orderStream.addSink(JdbcSink.sink(
                "CREATE TABLE IF NOT EXISTS sales_per_month (" +
                        "year INTEGER, " +
                        "month INTEGER, " +
                        "total_sales DOUBLE PRECISION, " +
                        "PRIMARY KEY (year, month)" +
                        ")",
                (JdbcStatementBuilder<Order>) (preparedStatement, order) -> {

                },
                execOptions,
                connOptions
        )).name("Create Sales Per Month Table");

        orderStream.addSink(JdbcSink.sink(
                "INSERT INTO transactions(order_id, product_id, product_name, product_category, product_price, " +
                        "product_quantity, product_brand, total_amount, currency, customer_id, order_date, payment_method) " +
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) " +
                        "ON CONFLICT (order_id) DO UPDATE SET " +
                        "product_id = EXCLUDED.product_id, " +
                        "product_name  = EXCLUDED.product_name, " +
                        "product_category  = EXCLUDED.product_category, " +
                        "product_price = EXCLUDED.product_price, " +
                        "product_quantity = EXCLUDED.product_quantity, " +
                        "product_brand = EXCLUDED.product_brand, " +
                        "total_amount  = EXCLUDED.total_amount, " +
                        "currency = EXCLUDED.currency, " +
                        "customer_id  = EXCLUDED.customer_id, " +
                        "order_date = EXCLUDED.order_date, " +
                        "payment_method = EXCLUDED.payment_method " +
                        "WHERE transactions.order_id = EXCLUDED.order_id",
                (JdbcStatementBuilder<Order>) (preparedStatement, order) -> {
                    preparedStatement.setString(1, order.getOrderId());
                    preparedStatement.setString(2, order.getProductId());
                    preparedStatement.setString(3, order.getProductName());
                    preparedStatement.setString(4, order.getProductCategory());
                    preparedStatement.setDouble(5, order.getProductPrice());
                    preparedStatement.setInt(6, order.getProductQuantity());
                    preparedStatement.setString(7, order.getProductBrand());
                    preparedStatement.setDouble(8, order.getTotalAmount());
                    preparedStatement.setString(9, order.getCurrency());
                    preparedStatement.setString(10, order.getCustomerId());
                    preparedStatement.setTimestamp(11, order.getOrderDate());
                    preparedStatement.setString(12, order.getPaymentMethod());
                },
                execOptions,
                connOptions
        )).name("Insert the data coming from the kafka topic into the transactions table");

        orderStream.map(
                order -> {
                    Date orderDate = new Date(order.getOrderDate().getTime());
                    String category = order.getProductCategory();
                    double totalSales = order.getTotalAmount();
                    return new SalesPerCategory(orderDate, category, totalSales);
                }
        ).keyBy(SalesPerCategory::getCategory)
                .reduce((salesPerCategory, t1) -> {
                    salesPerCategory.setTotalSales(salesPerCategory.getTotalSales() + t1.getTotalSales());
                    return salesPerCategory;
                }).addSink(JdbcSink.sink(
                "INSERT INTO sales_per_category(order_date, category, total_sales) " +
                        "VALUES (?, ?, ?) " +
                        "ON CONFLICT (order_date, category) DO UPDATE SET " +
                        "total_sales = EXCLUDED.total_sales " +
                        "WHERE sales_per_category.category = EXCLUDED.category " +
                        "AND sales_per_category.order_date = EXCLUDED.order_date",
                (JdbcStatementBuilder<SalesPerCategory>) (preparedStatement, salesPerCategory) -> {
                    preparedStatement.setDate(1, salesPerCategory.getOrderDate());
                    preparedStatement.setString(2, salesPerCategory.getCategory());
                    preparedStatement.setDouble(3, salesPerCategory.getTotalSales());
                },
                execOptions,
                connOptions
        )).name("Insert into sales per category table");

        orderStream.map(
                order -> {
                    Date orderDate = new Date(order.getOrderDate().getTime());
                    double totalSales = order.getTotalAmount();
                    return new SalesPerDay(orderDate, totalSales);
                }
        ).keyBy(SalesPerDay::getOrderDate)
                .reduce((salesPerDay, t1) -> {
                    salesPerDay.setTotalSales(salesPerDay.getTotalSales() + t1.getTotalSales());
                    return salesPerDay;
                }).addSink(JdbcSink.sink(
                "INSERT INTO sales_per_day(order_date, total_sales) " +
                        "VALUES (?,?) " +
                        "ON CONFLICT (order_date) DO UPDATE SET " +
                        "total_sales = EXCLUDED.total_sales " +
                        "WHERE sales_per_day.order_date = EXCLUDED.order_date",
                (JdbcStatementBuilder<SalesPerDay>) (preparedStatement, salesPerDay) -> {
                    preparedStatement.setDate(1, salesPerDay.getOrderDate());
                    preparedStatement.setDouble(2, salesPerDay.getTotalSales());
                },
                execOptions,
                connOptions
        )).name("Insert into sales per day table");

        orderStream.map(
                order -> {
                    Date orderDate = new Date(order.getOrderDate().getTime());
                    int year = orderDate.toLocalDate().getYear();
                    int month = orderDate.toLocalDate().getMonth().getValue();
                    double totalSales = order.getTotalAmount();
                    return new SalesPerMonth(year, month, totalSales);
                }
        ).keyBy(SalesPerMonth::getMonth)
                .reduce((salesPerMonth, t1) -> {
                    salesPerMonth.setTotalSales(salesPerMonth.getTotalSales() + t1.getTotalSales());
                    return salesPerMonth;
                }).addSink(JdbcSink.sink(
                "INSERT INTO sales_per_month(year, month, total_sales) " +
                        "VALUES (?,?,?) " +
                        "ON CONFLICT (year, month) DO UPDATE SET " +
                        "total_sales = EXCLUDED.total_sales " +
                        "WHERE sales_per_month.year = EXCLUDED.year " +
                        "AND sales_per_month.month = EXCLUDED.month ",
                (JdbcStatementBuilder<SalesPerMonth>) (preparedStatement, salesPerMonth) -> {
                    preparedStatement.setInt(1, salesPerMonth.getYear());
                    preparedStatement.setInt(2, salesPerMonth.getMonth());
                    preparedStatement.setDouble(3, salesPerMonth.getTotalSales());
                },
                execOptions,
                connOptions
        )).name("Insert into sales per month table");

        /*
         * No need anymore because of the lack of memory by running at the same time kafka, flink, elastic and kibana
         * So, try to figure out a better way to make a visualisation like a simple stuff with python just to show
         * some thing in browser let's do it Mohamed
         */

        /*orderStream.sinkTo(
                new Elasticsearch7SinkBuilder<Order>()
                        .setHosts(new HttpHost("localhost", 9200, "http"))
                        .setEmitter((order, runtimeContext, requestIndexer) -> {

                            String json = convertTransactionToJson(order);

                            IndexRequest indexRequest = Requests.indexRequest()
                                    .index("transactions")
                                    .id(order.getOrderId())
                                    .source(json, XContentType.JSON);
                            requestIndexer.add(indexRequest);
                        })
                        .build()
        ).name("Elasticsearch Sink");*/

        // Execute program, beginning computation.
        env.execute("Realtime Sales analytics");
    }
}
