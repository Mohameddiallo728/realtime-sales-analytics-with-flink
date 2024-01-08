package utils;


import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import models.Order;

/**
 * Created by mohamed on 12/21/23  at 12:24 AM
 **/
public class JsonUtil {
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static String convertTransactionToJson(Order order) {
        try {
            return objectMapper.writeValueAsString(order);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return null;
        }
    }
}
