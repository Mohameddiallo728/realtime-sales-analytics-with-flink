package models;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.sql.Date;

/**
 * Created by mohamed on 12/20/23  at 10:45 AM
 **/
@Data
@AllArgsConstructor
@NoArgsConstructor
public class SalesPerCategory implements Serializable {
    @JsonFormat(pattern = "yyyy-MM-dd")
    private Date orderDate;

    private String category;

    private Double totalSales;
}
