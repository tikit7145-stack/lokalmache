# 🔄 UPDATING ORDER STATUS - NEXT PHASE
# Mete Ajou Estati Kòmand - Faz Kap Vini

**Purpose:** Guide for implementing the order status update feature  
**Status:** PLANNING  
**Priority:** HIGH  

---

## 📋 TASKS TO IMPLEMENT

### Task 1: Add `update_order_status()` to database.py

Currently, the `OrderStatusManager.update_order_status()` method calls:
```python
result = db.update_order_status(order_id, new_status)
```

But this method doesn't exist in `src/database.py` yet.

**What to do:**
Add this method to the `SupabaseManager` class:

```python
def update_order_status(self, order_id, new_status):
    """Update order status in database"""
    try:
        from src.order_manager import OrderStatusManager
        
        # Validate status
        if new_status not in OrderStatusManager.STATUSES:
            return False
        
        # Update in Supabase
        response = self.client.table('orders').update({
            'status': new_status,
            'updated_at': datetime.now().isoformat()
        }).eq('id', order_id).execute()
        
        return bool(response.data)
    except Exception as e:
        print(f"❌ Error updating status: {e}")
        return False
```

---

### Task 2: Create UI Components for Status Updates

Add to `app.py` layout:

```python
html.Div(
    className="status-update-section",
    children=[
        html.H3("🔄 METE AJOU ESTATI KOMAND", className="chart-title"),
        
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "10px"},
            children=[
                html.Div([
                    html.Label("Seleksyon Komand:", className="input-label"),
                    dcc.Dropdown(
                        id="order-select-dropdown",
                        options=[],  # Will be populated with order IDs
                        placeholder="Seleksyon yon komand...",
                        className="dropdown-style"
                    ),
                ]),
                
                html.Div([
                    html.Label("Nouvo Estati:", className="input-label"),
                    dcc.Dropdown(
                        id="status-update-dropdown",
                        options=[
                            {"label": "⏳ Atant", "value": "pending"},
                            {"label": "✅ Konfime", "value": "confirmed"},
                            {"label": "🚚 Nan Wout", "value": "in_transit"},
                            {"label": "📦 Rive", "value": "delivered"},
                        ],
                        placeholder="Chwazi estati...",
                        className="dropdown-style"
                    ),
                ]),
                
                html.Div([
                    html.Label("", style={"opacity": "0"}),  # Spacer
                    html.Button(
                        "✏️ METE AJOU",
                        id="update-status-btn",
                        className="btn-update",
                        n_clicks=0,
                        style={
                            "padding": "10px 20px",
                            "backgroundColor": "rgba(100, 200, 255, 0.8)",
                            "color": "white",
                            "border": "none",
                            "borderRadius": "8px",
                            "cursor": "pointer",
                            "fontSize": "14px",
                            "fontWeight": "bold",
                            "width": "100%"
                        }
                    ),
                ]),
            ]
        ),
        
        # Status update confirmation message
        html.Div(
            id="status-update-message",
            style={
                "marginTop": "15px",
                "padding": "10px",
                "borderRadius": "8px",
                "textAlign": "center",
                "display": "none"
            }
        )
    ]
)
```

---

### Task 3: Add Callbacks to Handle Status Updates

Add to `app.py`:

```python
# Populate order dropdown
@callback(
    Output('order-select-dropdown', 'options'),
    Input('interval-component', 'n_intervals')
)
def update_order_options(n):
    """Populate dropdown with available orders"""
    orders = db.get_orders(limit=100)
    
    if orders.empty:
        return []
    
    options = [
        {
            "label": f"Order {str(row['id'])[:8]} - ${row['total_amount']:,.2f} ({row.get('user_name', 'Unknown')})",
            "value": str(row['id'])
        }
        for _, row in orders.iterrows()
    ]
    
    return options


# Handle status update button click
@callback(
    [Output('status-update-message', 'children'),
     Output('status-update-message', 'style'),
     Output('order-select-dropdown', 'value'),
     Output('status-update-dropdown', 'value')],
    Input('update-status-btn', 'n_clicks'),
    [State('order-select-dropdown', 'value'),
     State('status-update-dropdown', 'value')],
    prevent_initial_call=True
)
def handle_status_update(n_clicks, order_id, new_status):
    """Update order status when button is clicked"""
    if not n_clicks or not order_id or not new_status:
        raise PreventUpdate
    
    from src.order_manager import OrderStatusManager
    
    success, message = OrderStatusManager.update_order_status(order_id, new_status)
    
    style = {
        "marginTop": "15px",
        "padding": "10px",
        "borderRadius": "8px",
        "textAlign": "center",
        "display": "block",
        "color": "white",
        "backgroundColor": "#4CAF50" if success else "#F44336"
    }
    
    if success:
        message_text = f"✅ {message}"
    else:
        message_text = f"❌ {message}"
    
    return message_text, style, None, None
```

---

### Task 4: CSS Styling for Status Update UI

Add to `assets/style.css`:

```css
.status-update-section {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
    width: 100%;
}

.input-label {
    display: block;
    margin-bottom: 8px;
    color: rgba(200, 200, 200, 0.9);
    font-size: 14px;
    font-weight: 600;
}

.btn-update {
    background: linear-gradient(135deg, rgba(100, 200, 255, 0.8), rgba(100, 150, 255, 0.8));
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    transition: all 0.3s ease;
    width: 100%;
}

.btn-update:hover {
    background: linear-gradient(135deg, rgba(100, 200, 255, 1), rgba(100, 150, 255, 1));
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(100, 200, 255, 0.4);
}

.btn-update:active {
    transform: translateY(0px);
}

.status-update-message {
    padding: 10px;
    border-radius: 8px;
    text-align: center;
    margin-top: 15px;
    color: white;
    font-weight: 600;
}
```

---

### Task 5: Database Migration (if needed)

Check if the `orders` table has an `updated_at` column:

```sql
-- If not present, add it:
ALTER TABLE orders ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
```

Also ensure `status` column type and values are correct:

```sql
-- Check current column
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'orders' AND column_name = 'status';

-- Ensure it's varchar/text
ALTER TABLE orders 
ALTER COLUMN status TYPE VARCHAR(20);
```

---

## 📊 EXPECTED WORKFLOW

```
1. User selects order from dropdown
   ↓
2. User selects new status from dropdown
   ↓
3. User clicks "METE AJOU" button
   ↓
4. Callback triggers:
   - Validates order_id and new_status
   - Calls OrderStatusManager.update_order_status()
   - Updates database via db.update_order_status()
   ↓
5. Shows success/error message
   ↓
6. Auto-refresh (30s) reloads all status data
   ↓
7. Status cards and pie chart update automatically
```

---

## 🧪 TESTING PLAN

### Test 1: Update Single Order
```python
from src.order_manager import OrderStatusManager

# Get first pending order
pending_orders = OrderStatusManager.get_orders_by_status('pending')
if not pending_orders.empty:
    order_id = pending_orders.iloc[0]['id']
    
    # Update to confirmed
    success, msg = OrderStatusManager.update_order_status(order_id, 'confirmed')
    print(f"Updated: {msg}")
    
    # Verify
    updated = OrderStatusManager.get_orders_by_status('confirmed')
    print(f"Confirmed orders: {len(updated)}")
```

### Test 2: UI Form Submission
1. Open dashboard at http://localhost:8051
2. Scroll to "METE AJOU ESTATI KOMAND" section
3. Select an order from dropdown
4. Select new status
5. Click "METE AJOU" button
6. Verify success message appears
7. Check that status cards update

### Test 3: Auto-Refresh
1. Update an order status
2. Wait 30 seconds
3. Verify status counts change in real-time
4. Verify pie chart updates

---

## ⚠️ VALIDATION REQUIREMENTS

- [x] Order ID must exist in database
- [x] New status must be one of: pending, confirmed, in_transit, delivered
- [x] Status field must be updated in database
- [x] Updated timestamp should be recorded
- [x] Auto-refresh should reflect changes
- [x] Success message should display
- [x] Form should reset after successful update

---

## 🔐 SECURITY CONSIDERATIONS

1. **Authorization:** Add check to ensure only admin can update status
2. **Validation:** Validate order_id and new_status before update
3. **Audit Trail:** Log all status changes for compliance
4. **Rate Limiting:** Add delay between updates to prevent abuse

---

## 📱 MOBILE APP INTEGRATION

Once status updates are working in dashboard, mobile app can:

1. Display list of orders
2. Allow field agents to update status
3. Sync changes to Supabase
4. Dashboard updates in real-time

---

## ⏭️ PHASE 3: ORDER DETAILS PAGE

After Task 5 complete, implement:

1. Click on order → shows details page
2. Display full timeline of status changes
3. Show order items, amounts, customer info
4. History log of all status updates

---

## 📞 QUICK REFERENCE

**Current Status Summary:**
```
⏳ Atant: 25 kòmand
✅ Konfime: 8 kòmand
🚚 Nan Wout: 0 kòmand
📦 Rive: 9 kòmand
```

**File Locations:**
- Main app: `/app.py`
- Status manager: `/src/order_manager.py`
- Database: `/src/database.py`
- Components: `/src/components.py`
- CSS: `/assets/style.css`

**Import statements needed:**
```python
from dash import State
from dash.exceptions import PreventUpdate
from src.order_manager import OrderStatusManager
from src.database import get_supabase_manager
```

---

**Next Step:** Implement Task 1 (add `update_order_status()` to database.py)

