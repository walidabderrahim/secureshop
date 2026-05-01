const express = require('express');
const app = express();
app.use(express.json());

let inventory = [
  { product_id: 1, name: 'Laptop',     stock: 10 },
  { product_id: 2, name: 'Smartphone', stock: 25 },
  { product_id: 3, name: 'Book',       stock: 100 },
  { product_id: 4, name: 'Headphones', stock: 30 },
  { product_id: 5, name: 'Desk Chair', stock: 15 }
];

app.get('/inventory', (_req, res) => res.json(inventory));

app.get('/inventory/:product_id', (req, res) => {
  const item = inventory.find(i => i.product_id === parseInt(req.params.product_id));
  if (!item) return res.status(404).json({ error: 'Product not found' });
  return res.json(item);
});

app.post('/inventory/reserve', (req, res) => {
  const { product_id, quantity } = req.body;
  if (!product_id || !quantity)
    return res.status(400).json({ error: 'product_id and quantity required' });
  const item = inventory.find(i => i.product_id === parseInt(product_id));
  if (!item) return res.status(404).json({ error: 'Product not found' });
  if (item.stock < quantity)
    return res.status(400).json({ error: 'Insufficient stock', available: item.stock });
  item.stock -= parseInt(quantity);
  return res.json({ message: 'Stock reserved', remaining: item.stock });
});

app.post('/inventory/release', (req, res) => {
  const { product_id, quantity } = req.body;
  if (!product_id || !quantity)
    return res.status(400).json({ error: 'product_id and quantity required' });
  const item = inventory.find(i => i.product_id === parseInt(product_id));
  if (!item) return res.status(404).json({ error: 'Product not found' });
  item.stock += parseInt(quantity);
  return res.json({ message: 'Stock released', remaining: item.stock });
});

app.get('/health', (_req, res) =>
  res.json({ status: 'ok', service: 'inventory-service' }));

app.listen(8006, '0.0.0.0', () =>
  console.log('Inventory service running on port 8006'));
