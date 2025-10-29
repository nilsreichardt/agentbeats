# Demo

Number of sellers: 5
Number of consumers: 10

Actions that sellers can take:
- Create a product (only at the beginning of a round)
- Edit product name
- Change product description
- Change product image
- Change price
- Do nothing

Actions that consumers can take:
- Buy a product
- Do nothing

## Example:

* Spinning up database (wait 1 sec)
* Spinning up Marketplace API (wait 1 sec)
* Environment ready (wait 0.5 sec)
* Starting round 1 (wait 0.2 sec)
* White Agents can now create products (wait 0.2 sec)
* Seller 1 created product "Product 1" (wait 0.1 sec)
* Seller 2 created product "Product 2" (wait 0.2 sec)
* Seller 3 created product "Product 3" (wait 0.1 sec)
* Every seller created a product. Going to the next phase (wait 0.2 sec)
* Starting day 1 (wait 0.2 sec)
* Using random order for products since it's the first day (wait 5 sec)
* Consumer can now buy products (wait 5 sec)
* Consumer 1 bought Product 1 (wait 2 sec)
* Consumer 2 decided not to buy anything (wait 2 sec)
* Consumer 3 bought Product 3 (wait 2 sec)
* Every consumer made their decision. Going to the next phase (wait 0.2 sec)
* Starting day 2 (wait 0.2 sec)
* Seller can now edit their product pages (wait 0.2 sec)
* Seller 2 edited their product name (wait 2 sec)
* Seller 1 edited their product name (wait 1 sec)
* Seller 2 changed the price of their product (wait 1.5 sec)
* Seller 3 decided not to edit their product name (wait 1.5 sec)
* Every seller made their decision. Going to the next phase (wait 0.2 sec)
* Consumer can now buy products (wait 5 sec)
* Consumer 1 decided not to buy anything (wait 2 sec)
* Consumer 2 bought Product 2 (wait 2 sec)
* Consumer 3 decided not to buy anything (wait 2 sec)
* Every consumer made their decision. Going to the next phase (wait 0.2 sec)
* Starting day 3 (wait 0.2 sec)
* Seller can now edit their product pages (wait 0.2 sec)
* Seller 2 changed the price of their product (wait 2 sec)
* Seller 1 changed the price of their product (wait 1 sec)
* Seller 3 decided not to edit their product page (wait 1.5 sec)
* Every seller made their decision. Going to the next phase (wait 0.2 sec)
* Consumer can now buy products (wait 5 sec)
* Consumer 1 decided not to buy anything (wait 2 sec)
* Consumer 2 bought Product 2 (wait 2 sec)
* Consumer 3 decided not to buy anything (wait 2 sec)
* Every consumer made their decision. Going to the next phase (wait 0.2 sec)
* Round 1 finished (wait 0.2 sec)
* Winner of round 1: Seller 2 (wait 0.2 sec)
* Round 2 started (wait 0.2 sec)
...
* Winner of round 2: Seller 2 (wait 0.2 sec)
* Round 3 started (wait 0.2 sec)
...
* Winner of round 3: Seller 2 (wait 0.2 sec)
* Calculating average of all rounds (wait 0.2 sec)
* Seller 2 is the overall winner (wait 0.2 sec)
* | Seller | Avg Revenue | Total Revenue |
  | Seller 2 | 100 | 300 |
  | Seller 1 | 50 | 150 |
   ...