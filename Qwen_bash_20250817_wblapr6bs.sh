curl -X POST http://localhost:5000/api/convert \
  -H "Content-Type: application/json" \
  -d '{
    "value": 10,
    "from_unit": "lbna_sanaani",
    "to_unit": "faddan"
  }'