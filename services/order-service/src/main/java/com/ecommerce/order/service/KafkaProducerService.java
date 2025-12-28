package com.ecommerce.order.service;

import com.ecommerce.order.model.Order;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class KafkaProducerService {

    private final KafkaTemplate<String, Object> kafkaTemplate;
    private static final String TOPIC_ORDER_CREATED = "order-created";

    public void publishOrderCreatedEvent(Order order) {
        log.info("Publishing order-created event for Order Number: {}", order.getOrderNumber());

        Map<String, Object> eventData = new HashMap<>();
        eventData.put("order_id", order.getOrderNumber());
        eventData.put("user_id", order.getUserId());
        eventData.put("total_amount", order.getTotalAmount());
        eventData.put("status", order.getStatus());
        
        // Map items
        var items = order.getOrderItems().stream().map(item -> {
            Map<String, Object> itemMap = new HashMap<>();
            itemMap.put("product_id", item.getProductId());
            itemMap.put("quantity", item.getQuantity());
            return itemMap;
        }).collect(Collectors.toList());
        
        eventData.put("items", items);

        kafkaTemplate.send(TOPIC_ORDER_CREATED, order.getOrderNumber(), eventData);
        log.info("Event published successfully");
    }
}
