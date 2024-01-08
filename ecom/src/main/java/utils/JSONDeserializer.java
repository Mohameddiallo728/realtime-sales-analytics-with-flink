package utils;

import com.fasterxml.jackson.databind.ObjectMapper;
import models.Order;
import org.apache.flink.api.common.serialization.DeserializationSchema;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.util.Collector;

import java.io.IOException;

/**
 * Created by mohamed on 12/20/23  at 2:02 PM
 **/
public class JSONDeserializer implements DeserializationSchema<Order> {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public void open(InitializationContext context) throws Exception {
        DeserializationSchema.super.open(context);
    }

    @Override
    public Order deserialize(byte[] bytes) throws IOException {
        return objectMapper.readValue(bytes, Order.class);
    }

    @Override
    public void deserialize(byte[] message, Collector<Order> out) throws IOException {
        DeserializationSchema.super.deserialize(message, out);
    }

    @Override
    public boolean isEndOfStream(Order order) {
        return false;
    }

    @Override
    public TypeInformation<Order> getProducedType() {
        return TypeInformation.of(Order.class);
    }
}
