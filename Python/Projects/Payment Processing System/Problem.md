# Payment Processing System

## Concepts
- **Abstraction**
- **Inheritance** 
- **Polymorphism**
- **Encapsulation**

## Scenario

You're building a payment system that supports multiple payment methods:

### Payment Methods
- **Credit Card**
- **UPI**
- **Wallet**

### Core Payment Operations
All payment methods must:
1. **Validate** the payment details
2. **Deduct balance** from the source
3. **Return transaction status**

## Requirements

### Base Implementation
- Create an **abstract base class** `PaymentMethod`

### Concrete Implementations
- `CreditCardPayment`
- `UPIPayment`
- `WalletPayment`

### Key Features
- Each payment type has its own **validation logic**
- A single `process_payment()` method should work for all types (**polymorphism**)

## Extensions ⚠️ **Very Important**

### Additional Features to Implement
1. **Retry logic** - Handle failed transactions with retry mechanisms
2. **Failure reasons** - Provide detailed error messages
3. **Logging hooks** - Add comprehensive logging for debugging and monitoring

### Key Design Principle
> **"Open for extension, closed for modification"**
> 
> The system should be easily extensible for new payment methods without modifying existing code.