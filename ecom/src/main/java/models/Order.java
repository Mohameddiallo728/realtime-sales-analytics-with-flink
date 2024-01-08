package models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.sql.Timestamp;

/**
 * Created by mohamed on 12/20/23  at 10:39 AM
 **/
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Order implements Serializable {

    private String orderId;

    private String productId;

    private String productName;

    private String productCategory;

    private Double productPrice;

    private Integer productQuantity;

    private String productBrand;

    private String currency;

    private String customerId;

    private Timestamp orderDate;

    private String paymentMethod;

    private Double totalAmount;
}
