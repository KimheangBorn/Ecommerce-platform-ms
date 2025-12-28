package com.ecommerce.order.service;

import com.ecommerce.order.dto.CreateOrderRequest;
import com.ecommerce.order.model.Order;
import com.ecommerce.order.model.OrderItem;
import com.ecommerce.order.repository.OrderRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class OrderService {

    private final OrderRepository orderRepository;
    private final KafkaProducerService kafkaProducerService;

    // In a real scenario, we would inject a ProductServiceClient here
    // For now, we'll mock the price fetch or assume a fixed price for simplicity
    // given we don't have the Feign client set up yet.

    @Transactional
    public Order createOrder(CreateOrderRequest request) {
        log.info("Creating order for user: {}", request.getUserId());

        // 1. Create Order object
        Order order = Order.builder()
                .orderNumber(UUID.randomUUID().toString())
                .userId(request.getUserId())
                .status("PENDING")
                .build();

        // 2. Map items and calculate total
        // Note: Realistically we should fetch current prices from Product Service via REST/Feign
        // Here assuming a fixed price of 10.00 for demo purposes to avoid blocking on REST client setup
        BigDecimal mockPrice = new BigDecimal("10.00"); 

        List<OrderItem> orderItems = request.getItems().stream().map(itemDto -> {
            BigDecimal subtotal = mockPrice.multiply(BigDecimal.valueOf(itemDto.getQuantity()));
            return OrderItem.builder()
                    .productId(itemDto.getProductId())
                    .quantity(itemDto.getQuantity())
                    .price(mockPrice)
                    .subtotal(subtotal)
                    .order(order)
                    .build();
        }).collect(Collectors.toList());

        order.setOrderItems(orderItems);
        
        BigDecimal totalAmount = orderItems.stream()
                .map(OrderItem::getSubtotal)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        order.setTotalAmount(totalAmount);

        // 3. Save to DB
        Order savedOrder = orderRepository.save(order);
        log.info("Order saved with ID: {}", savedOrder.getId());

        // 4. Publish Event
        kafkaProducerService.publishOrderCreatedEvent(savedOrder);

        return savedOrder;
    }

    public List<Order> getUserOrders(Long userId) {
        return orderRepository.findByUserId(userId);
    }
    
    public Order getOrder(Long id) {
        return orderRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Order not found"));
    }
}
