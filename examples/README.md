# 🚀 Neodoo18Framework - Practical Examples

> **Real-world examples and use cases**

## 📋 **AVAILABLE EXAMPLES**

### 🛍️ **E-commerce Examples**
- **Simple Store** - Basic product management
- **Multi-vendor** - Marketplace functionality
- **Digital Products** - Downloads and licenses

### 📚 **Business Management**
- **Library System** - Books, authors, borrowing
- **School Management** - Students, teachers, grades
- **Hospital Management** - Patients, doctors, appointments

### 💰 **Financial Applications**
- **Expense Tracker** - Personal finance
- **Invoice System** - Billing and payments
- **Budget Planner** - Financial planning

### 🏭 **Industry Specific**
- **Manufacturing** - Production planning
- **Real Estate** - Property management
- **Restaurant** - POS and inventory

---

## 💡 **HOW TO USE EXAMPLES**

### Method 1: Visual Interface (Recommended)
```bash
# Use the interactive menu
./neodoo                          # Select "Create new project"
# 1. Choose template based on your example
# 2. Follow visual wizard
# 3. Copy example code to your project

# Copy example code
cp examples/library_system/* ~/odoo_projects/your_project/custom_addons/

# Validate using menu
./neodoo                          # Select "Environment check"
```

### Method 2: Direct Generation
```bash
# Generate from templates with visual feedback
./neodoo create --name library_system --template minimal
cd ~/odoo_projects/library_system

# Copy example code
cp examples/library_system/* custom_addons/

# Validate
python3 framework/validator.py custom_addons/
```

### Method 3: AI Development
```bash
# Create base project with visual interface
./neodoo create --name my_restaurant --template advanced

# Use examples as reference for AI
cat examples/restaurant_pos/README.md

# Share with ChatGPT/Claude for development
```

---

## 📖 **EXAMPLE STRUCTURE**

Each example includes:
- **README.md** - Description and requirements
- **models/** - Data models
- **views/** - UI definitions
- **security/** - Access rules
- **data/** - Demo data
- **tests/** - Unit tests

---

## 🎯 **QUICK START WITH EXAMPLES**

```bash
# Clone framework
git clone https://github.com/neoand/neodoo18framework.git
cd neodoo18framework

# List available examples
ls examples/

# Generate project based on example
./neodoo create --name my_library --template minimal

# Or copy manually
cp -r examples/library_system ./my_library
```

---

## 📚 **LEARNING PATH**

### 🥉 **Beginner Examples**
1. **Simple Store** - Basic CRUD operations
2. **Contact Manager** - Partner inheritance
3. **Task Tracker** - Workflow states

### 🥈 **Intermediate Examples**
1. **Library System** - Complex relationships
2. **School Management** - Multi-model integration  
3. **Expense Tracker** - Financial calculations

### 🥇 **Advanced Examples**
1. **Manufacturing** - Complex workflows
2. **Multi-vendor Marketplace** - Advanced security
3. **Hospital Management** - Critical systems

---

## 🔧 **CUSTOMIZATION GUIDE**

### Adapting Examples:
1. **Copy base structure**
2. **Modify models** according to needs
3. **Update views** and menus
4. **Adjust security** rules
5. **Validate** with framework

### Best Practices:
- Follow Odoo 18+ standards
- Use framework validation
- Test thoroughly
- Document changes

---

## 📞 **CONTRIBUTE EXAMPLES**

Have a great example? Share with the community:

1. **Fork** repository
2. **Add** your example to `examples/`
3. **Follow** structure standards
4. **Submit** Pull Request
5. **Help** others learn!

---

**🚀 Happy Learning!**