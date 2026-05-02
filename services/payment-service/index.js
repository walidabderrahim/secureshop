const express = require('express');
const { v4: uuidv4 } = require('uuid');
const app = express();
app.use(express.json());
const transactions = [];
app.disable('x-powered-by');
app.post('/pay', (req, res) => {
  const { order_id, amount } = req.body;
  if (!order_id || !amount)
    return res.status(400).json({ error: 'order_id and amount required' });
  if (typeof amount !== 'number' || amount <= 0)
    return res.status(400).json({ error: 'amount must be a positive number' });
  const tx = { id: uuidv4(), order_id, amount, status: 'success',
               created_at: new Date().toISOString() };
  transactions.push(tx);
  return res.status(201).json(tx);
});

app.get('/transactions/:id', (req, res) => {
  const tx = transactions.find(t => t.id === req.params.id);
  if (!tx) return res.status(404).json({ error: 'Transaction not found' });
  return res.json(tx);
});

app.get('/transactions', (_req, res) => res.json(transactions));

app.get('/health', (_req, res) =>
  res.json({ status: 'ok', service: 'payment-service' }));

app.listen(8004, '0.0.0.0', () =>
  console.log('Payment service running on port 8004'));
