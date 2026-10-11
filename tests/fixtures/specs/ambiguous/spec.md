# Feature Specification: Shopping Cart

**Feature Branch**: `001-demo`

**Created**: 2026-10-11

**Status**: Draft

**Input**: User description: "Let shoppers keep items in a cart and check out."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add items to a cart (Priority: P1)

A shopper adds products to a cart and sees a running total.

**Acceptance Scenarios**:

1. **Given** an empty cart, **When** the shopper adds a product, **Then** the cart shows it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The cart MUST keep items for a reasonable time.
- **FR-002**: The system MUST support a sensible number of items per cart.
- **FR-003**: A discount MAY apply at checkout, in a way to be decided.
- **FR-004**: Prices MUST be shown in the shopper's currency.

### Key Entities

- **Cart**: the items a shopper intends to buy.
- **Shopper**: a person using the shop; sometimes called a customer or a user.

## Success Criteria *(mandatory)*

- **SC-001**: Shoppers check out quickly.
