# 📚 Library Management System

> **Complete library management with books, authors, and borrowing**

## 🎯 **OVERVIEW**

This example demonstrates a complete library management system using Neodoo18Framework with:
- **Books**: Title, author, ISBN, category
- **Authors**: Name, biography, nationality  
- **Borrowing**: User loans and returns
- **Categories**: Book classification
- **Reports**: Borrowing statistics

## 🏗️ **FEATURES**

### 📖 **Book Management**
- ✅ Complete book catalog
- ✅ ISBN validation and uniqueness
- ✅ Category classification
- ✅ Availability tracking
- ✅ Multi-author support

### 👤 **Member Management**
- ✅ Library member registration
- ✅ Contact information management
- ✅ Borrowing history
- ✅ Member status tracking

### 🔄 **Borrowing System**
- ✅ Book checkout process
- ✅ Return management
- ✅ Due date tracking
- ✅ Late return penalties
- ✅ Reservation system

### 📊 **Reporting**
- ✅ Popular books report
- ✅ Member statistics
- ✅ Overdue items tracking
- ✅ Inventory reports

## 🚀 **QUICK SETUP**

### Using Framework Generator:
```bash
# Create project
./quick-start.sh my_library

# Copy example files
cp -r examples/library_system/* my_library/

# Validate
python3 framework/validator.py my_library/
```

### Manual Setup:
```bash
# Create directory
mkdir my_library
cd my_library

# Copy all files from this example
cp -r ../examples/library_system/* .

# Review and customize as needed
```

## 📋 **MODELS INCLUDED**

### 🏗️ **Core Models**

#### `bjj.book` - Book Model
```python
class Book(models.Model):
    _name = 'bjj.book'
    _description = 'Library Book'
    
    title = fields.Char(required=True)
    isbn = fields.Char(size=13)
    author_ids = fields.Many2many('bjj.author')
    category_id = fields.Many2one('bjj.book.category')
    available = fields.Boolean(default=True)
```

#### `bjj.author` - Author Model
```python
class Author(models.Model):
    _name = 'bjj.author'
    _description = 'Book Author'
    
    name = fields.Char(required=True)
    biography = fields.Text()
    nationality = fields.Char()
    book_ids = fields.Many2many('bjj.book')
```

#### `bjj.borrowing` - Borrowing Model
```python
class Borrowing(models.Model):
    _name = 'bjj.borrowing'
    _description = 'Book Borrowing'
    
    member_id = fields.Many2one('res.partner')
    book_id = fields.Many2one('bjj.book')
    borrow_date = fields.Date(default=fields.Date.today)
    return_date = fields.Date()
    due_date = fields.Date()
    state = fields.Selection([
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue')
    ])
```

## 🎨 **VIEWS STRUCTURE**

### 📋 **List Views**
- Books list with search and filters
- Authors with book count
- Borrowings with status indication
- Members with borrowing statistics

### 📝 **Form Views**  
- Book form with all details
- Author profile with biography
- Borrowing form with dates
- Member information

### 📊 **Kanban Views**
- Books by category
- Borrowings by status
- Popular books dashboard

## 🔒 **SECURITY SETUP**

### User Groups:
- **Librarian**: Full access to all features
- **Assistant**: Limited access to borrowing
- **Member**: Read-only access to catalog

### Access Rules:
- Members can only see available books
- Staff can manage all records
- Administrators have full system access

## 📊 **DEMO DATA**

Includes sample data for:
- 50+ books across multiple categories
- 20+ authors with biographies
- 10+ library members
- Active borrowing records
- Categories and classifications

## 🧪 **TESTING**

### Test Coverage:
- Book creation and validation
- ISBN uniqueness constraints
- Borrowing workflow
- Date calculations
- Security access rules

### Run Tests:
```bash
# Install module with demo data
# Go to Odoo Apps → Install "Library Management"

# Test functionality:
# 1. Create books and authors
# 2. Register library members  
# 3. Process book borrowing
# 4. Generate reports
```

## 🔧 **CUSTOMIZATION IDEAS**

### Extensions:
- **Digital Books**: PDF/ebook management
- **Reservations**: Book reservation system
- **Fines**: Late return penalty calculation
- **Reviews**: Book rating and reviews
- **Events**: Library events management

### Integration:
- **Email**: Automatic due date reminders
- **Barcode**: ISBN barcode scanning
- **Reports**: Advanced analytics
- **Mobile**: Mobile app integration

## 📚 **LEARNING OBJECTIVES**

This example teaches:
- ✅ **Model Relationships**: Many2many, Many2one
- ✅ **Computed Fields**: Availability, overdue status
- ✅ **Workflow States**: Borrowing lifecycle
- ✅ **Constraints**: ISBN validation, date logic
- ✅ **Security**: Multi-level access control
- ✅ **Views**: List, form, kanban patterns
- ✅ **Reports**: Data analysis and presentation

## 🎯 **NEXT STEPS**

1. **Deploy**: Copy to Odoo addons and install
2. **Customize**: Adapt to your library needs
3. **Extend**: Add new features and integrations
4. **Scale**: Handle multiple library branches
5. **Integrate**: Connect with other systems

## 🤝 **AI DEVELOPMENT**

### For ChatGPT/Claude:
```
Using this library system example from Neodoo18Framework:

1. Review the model structure in models/
2. Follow the view patterns in views/
3. Maintain Odoo 18+ compliance (<list> not <tree>)
4. Use the SOIL system guidance
5. Validate with framework tools

Create an enhancement for [your specific need]
```

---

**📚 Happy Library Management! 📖**