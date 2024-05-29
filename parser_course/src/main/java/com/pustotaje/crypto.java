package com.pustotaje;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class crypto {

    public static void main(String[] args) {
        try {
            String response = sendGetRequest("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,
            ETH,TONCOIN,BNB,MATIC,TRX,XRP,LTC,SHIB,DOGE&tsyms=USD&api_key=c9acbd141db2f6c9a6411c6c848f0e60ada52abbf5f3914bd9327f1816d2b37b");
            processResponse(response);
        } catch (IOException | JSONException e) {
            e.printStackTrace();
        }
    }

    private static String sendGetRequest(String urlString) throws IOException {
        StringBuilder response = new StringBuilder();

        URL url = new URL(urlString);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");

        int responseCode = connection.getResponseCode();
        if (responseCode == HttpURLConnection.HTTP_OK) {
            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
        }

        return response.toString();
    }

    private static void processResponse(String response) throws JSONException {
        JSONObject jsonResponse = new JSONObject(response);

        JSONObject rawObject = jsonResponse.getJSONObject("RAW");
        JSONArray currencies = rawObject.names();

        for (int i = 0; i < currencies.length(); i++) {
            String currency = currencies.getString(i);
            JSONObject currencyObject = rawObject.getJSONObject(currency).getJSONObject("USD");
            String fromSymbol = currencyObject.getString("FROMSYMBOL");
            double price = currencyObject.getDouble("PRICE");
            double changeDay = currencyObject.getDouble("CHANGEDAY");
            double changePctDay = currencyObject.getDouble("CHANGEPCTDAY");

            System.out.println("Currency: " + fromSymbol);
            System.out.println("Price: " + price);
            System.out.println("Change Day: " + changeDay);
            System.out.println("Change Pct Day: " + changePctDay);
            System.out.println();
        }
    }
}