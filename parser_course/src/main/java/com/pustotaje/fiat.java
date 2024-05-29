package com.pustotaje;
import java.net.URL;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class fiat {
    private static String URL = "https://www.cbr-xml-daily.ru/daily_json.js";
    public static void main(String[] args) throws IOException {
            
            double CurUSDValue = getCurUSDValue();
            double CurEURValue = getCurEURValue();
            double CurCNYValue = getCurCNYValue();

            double oldUSDValue = getOldUSDValue();
            double oldEURValue = getOldEURValue();
            double oldCNYValue = getOldCNYValue();

            double PercentUSD = compareData(oldUSDValue, CurUSDValue);
            double PercentEUR = compareData(oldEURValue, CurEURValue);
            double PercentCNY = compareData(oldCNYValue, CurCNYValue);

            double diffUSD = oldUSDValue - CurUSDValue;
            double diffEUR = oldEURValue - CurEURValue;
            double diffCNY = oldCNYValue - CurCNYValue;

            System.out.println(CurUSDValue);
            System.out.println(diffUSD);
            System.out.println(PercentUSD);

            System.out.println(CurEURValue);
            System.out.println(diffEUR);
            System.out.println(PercentEUR);

            System.out.println(CurCNYValue);
            System.out.println(diffCNY);
            System.out.println(PercentCNY);
}   
public static double getCurUSDValue() {
    try {
        URL url = new URL(URL);
        BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            sb.append(line);
        }
        reader.close();
        
        JSONObject jsonObject = new JSONObject(sb.toString());
        JSONObject usdObject = jsonObject.getJSONObject("Valute").getJSONObject("USD");
        double usdValue = usdObject.getDouble("Value");
        
        return usdValue;
    } catch (Exception e) {
        e.printStackTrace();
        return 0.0; // Return a default value or handle the exception as needed
    }
}  
public static double getCurEURValue() {
    try {
        URL url = new URL(URL);
        BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            sb.append(line);
        }
        reader.close();
        
        JSONObject jsonObject = new JSONObject(sb.toString());
        JSONObject eurObject = jsonObject.getJSONObject("Valute").getJSONObject("EUR");
        double eurValue = eurObject.getDouble("Value");
        
        return eurValue;
    } catch (Exception e) {
        e.printStackTrace();
        return 0.0; // Return a default value or handle the exception as needed
    }
} 
public static double getCurCNYValue() {
    try {
        URL url = new URL(URL);
        BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            sb.append(line);
        }
        reader.close();
        
        JSONObject jsonObject = new JSONObject(sb.toString());
        JSONObject cnyObject = jsonObject.getJSONObject("Valute").getJSONObject("CNY");
        double cnyValue = cnyObject.getDouble("Value");
        
        return cnyValue;
    } catch (Exception e) {
        e.printStackTrace();
        return 0.0; // Return a default value or handle the exception as needed
    }
}  
public static double getOldUSDValue() {
    try {
    URL url = new URL(URL);
    BufferedReader reader= new BufferedReader(new InputStreamReader(url.openStream()));
    StringBuilder sb= new StringBuilder();
    String line;
    
       while ((line=reader.readLine())!=null) {
           sb.append(line);
        }
        
        reader.close();
    
        JSONObject jsonObject=new JSONObject(sb.toString());
        JSONObject usdObject=jsonObject.getJSONObject("Valute").getJSONObject("USD");
        double usdValue=usdObject.getDouble("Previous");
    
          return usdValue;
     } catch(Exception e) { 
         e.printStackTrace(); 
         return 0.0; // Возвращаемое значение по умолчанию или обработка исключения при необходимости
     }
    }
public static double getOldEURValue() {
        try {
            URL url = new URL(URL);
            BufferedReader reader= new BufferedReader(new InputStreamReader(url.openStream()));
            StringBuilder sb= new StringBuilder();
            String line;
            
            while ((line=reader.readLine())!=null) {
                sb.append(line);
            }
            
            reader.close();
    
            JSONObject jsonObject=new JSONObject(sb.toString());
          JSONObject eurObject=jsonObject.getJSONObject("Valute").getJSONObject("EUR");
           double eurValue=eurObject.getDouble("Previous");
    
              return eurValue;
         } catch(Exception e) { 
             e.printStackTrace(); 
             return 0.0; // Возвращаемое значение по умолчанию или обработка исключения при необходимости
         }
         }
public static double getOldCNYValue() {
    try {
        URL url = new URL(URL);
        BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            sb.append(line);
        }
        reader.close();
        
        JSONObject jsonObject = new JSONObject(sb.toString());
        JSONObject cnyObject = jsonObject.getJSONObject("Valute").getJSONObject("CNY");
        double cnyValue = cnyObject.getDouble("Previous");
        
        return cnyValue;
    } catch (Exception e) {
        e.printStackTrace();
        return 0.0; // Return a default value or handle the exception as needed
    }
}    
public static double compareData(double oldValue, double newValue) {
    double percentChange = 0;
    if (oldValue > newValue) {
        percentChange = -((oldValue / newValue) - 1) * 100;
    } else if (newValue > oldValue) {
        percentChange = ((newValue / oldValue) - 1) * 100;
    } else {
        percentChange = 0;
    }
    return percentChange;
}
}