const express = require('express');
const app = express();
app.use(express.json());
const orders = [];
let nextId = 1;
app.disable('x-powered-by');
app.post('/orders', (req, res) => {
  const { user_id, product_id, quantity } = req.body;
  if (!user_id || !product_id || !quantity)
    return res.status(400).json({ error: 'user_id, product_id and quantity required' });
  const order = {
    id: nextId++, user_id: parseInt(user_id),
    product_id: parseInt(product_id), quantity: parseInt(quantity),
    status: 'pending', created_at: new Date().toISOString()
  };
  orders.push(order);
  return res.status(201).json(order);
});

app.get('/orders/:id', (req, res) => {
  const order = orders.find(o => o.id === parseInt(req.params.id));
  if (!order) return res.status(404).json({ error: 'Order not found' });
  return res.json(order);
});

app.get('/orders', (_req, res) => res.json(orders));

app.get('/health', (_req, res) =>
  res.json({ status: 'ok', service: 'order-service' }));

app.listen(8003, '0.0.0.0', () =>
  console.log('Order service running on port 8003'));
