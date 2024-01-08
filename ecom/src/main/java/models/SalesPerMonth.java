package models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * Created by mohamed on 12/20/23  at 10:45 AM
 **/
@Data
@AllArgsConstructor
@NoArgsConstructor
public class SalesPerMonth implements Serializable {

    private Integer year;
    private Integer month;
    private Double totalSales;
}
