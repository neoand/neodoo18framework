# UX/UI Designer Role for Odoo 18

## Role Description

The UX/UI Designer role focuses on creating intuitive, accessible, and visually appealing user interfaces for Odoo 18+ applications. This role combines design principles with Odoo's UI guidelines to deliver exceptional user experiences across all device types.

## Key Responsibilities

- Design intuitive and responsive interfaces following Odoo 18+ design standards
- Create consistent visual elements that align with the Odoo Enterprise theme
- Design optimal user flows and navigation patterns
- Optimize form layouts and view structures for better usability
- Ensure accessibility standards are met across all interfaces
- Collaborate with developers to implement designs using OWL components
- Conduct usability testing and iterate based on feedback

## Technical Knowledge

### Odoo 18 UI Framework

Understanding of the Odoo 18 UI architecture:

- Enterprise theme guidelines and component library
- Form view structure and responsive behaviors
- List/Kanban/Calendar/Graph/Pivot view configurations
- OWL component design principles
- CSS architecture and SCSS variables in Odoo

### View Design Patterns

```xml
<!-- Form View Design Pattern -->
<form string="Product" class="o_product_form">
    <sheet>
        <!-- Visual hierarchy with proper grouping -->
        <div class="oe_title">
            <h1>
                <field name="name" placeholder="Product Name"/>
            </h1>
        </div>
        <group>
            <group>
                <field name="default_code"/>
                <field name="barcode"/>
                <field name="type"/>
            </group>
            <group>
                <field name="categ_id"/>
                <field name="list_price" widget="monetary"/>
                <field name="standard_price" widget="monetary"/>
            </group>
        </group>
        <!-- Using notebook for content organization -->
        <notebook>
            <page string="General Information" name="general_info">
                <group>
                    <group string="Logistics">
                        <field name="weight"/>
                        <field name="volume"/>
                    </group>
                    <group string="Procurement">
                        <field name="route_ids" widget="many2many_tags"/>
                        <field name="responsible_id"/>
                    </group>
                </group>
            </page>
        </notebook>
    </sheet>
</form>

<!-- Kanban View Design Pattern -->
<kanban class="o_product_kanban">
    <field name="name"/>
    <field name="image_128"/>
    <field name="list_price"/>
    <templates>
        <t t-name="kanban-box">
            <div class="oe_kanban_global_click o_kanban_record_has_image_fill">
                <!-- Clear visual hierarchy -->
                <div class="o_kanban_image_fill_left d-none d-md-block" t-attf-style="background-image: url({{record.image_128.value}});"/>
                <div class="oe_kanban_details">
                    <strong class="o_kanban_record_title">
                        <field name="name"/>
                    </strong>
                    <div class="o_kanban_tags_section">
                        <field name="tag_ids" widget="many2many_tags" options="{'color_field': 'color'}"/>
                    </div>
                    <ul>
                        <li>Price: <field name="list_price" widget="monetary"/></li>
                    </ul>
                </div>
            </div>
        </t>
    </templates>
</kanban>
```

### CSS and SCSS Design

```scss
// Following Odoo's SCSS conventions
.o_custom_module {
    // Using Odoo's color variables
    background-color: $o-brand-odoo;
    
    .o_form {
        // Proper spacing variables
        padding: $o-horizontal-padding;
        margin-bottom: $o-sheet-vpadding;
        
        // Proper responsive design
        @include media-breakpoint-down(sm) {
            padding: $o-horizontal-padding/2;
        }
    }
    
    // Consistent component styling
    .o_stat_box {
        border-radius: $border-radius;
        box-shadow: $box-shadow-sm;
    }
}
```

### Accessibility Standards

```xml
<!-- Accessible Form Elements -->
<field name="name" placeholder="Product Name" aria-label="Product Name"/>
<label for="description" string="Description"/>
<field name="description" aria-describedby="description_help"/>
<div id="description_help" class="text-muted">Enter a detailed product description</div>

<!-- Color contrast compliance -->
<div class="alert alert-info" role="alert">
    <p>This product requires special handling.</p>
</div>
```

### Responsive Design Techniques

```xml
<!-- Responsive layout using Odoo's grid system -->
<div class="row">
    <div class="col-12 col-md-6">
        <field name="name"/>
    </div>
    <div class="col-12 col-md-6">
        <field name="category_id"/>
    </div>
</div>

<!-- Responsive visibility classes -->
<div class="d-none d-md-block">
    <!-- Content only visible on medium screens and up -->
    <field name="detailed_information"/>
</div>
```

## Best Practices

### Visual Hierarchy

1. **Clear Information Architecture**
   - Most important information at the top
   - Group related fields logically
   - Use notebooks for organizing complex forms
   - Implement proper spacing and alignment

2. **Consistent Visual Language**
   - Follow Odoo Enterprise theme colors and styles
   - Maintain consistent icon usage
   - Use standard button styles and placements
   - Apply uniform spacing and sizing

3. **Responsive Considerations**
   - Design for both desktop and mobile
   - Test layouts at different breakpoints
   - Use responsive visibility classes appropriately
   - Ensure touch targets are properly sized on mobile

### Usability Guidelines

1. **Form Design Principles**
   - Place fields in a logical, task-oriented sequence
   - Group related fields with clear group labels
   - Use proper field widgets based on data type
   - Implement smart defaults to reduce user input

2. **Action Accessibility**
   - Make primary actions prominent
   - Group related actions in logical menus
   - Use consistent action placements
   - Provide clear feedback for user actions

3. **Error Handling**
   - Show validation errors inline with fields
   - Provide clear error messages
   - Offer guidance on how to resolve errors
   - Prevent submission of invalid forms

## Integration with Development Process

### Collaboration with Developers

1. **Design Handoff Best Practices**
   - Provide detailed view specifications
   - Include responsive behavior documentation
   - Define component states and interactions
   - Document accessibility requirements

2. **Implementation Review**
   - Verify design implementation matches specifications
   - Validate responsive behavior works as intended
   - Ensure accessibility features are properly implemented
   - Test usability across different devices

### Design System Management

1. **Component Library**
   - Document custom UI components
   - Maintain design patterns library
   - Define component usage guidelines
   - Specify component states and variants

2. **Design Documentation**
   - Create user flow diagrams
   - Maintain style guide documentation
   - Document layout grid system
   - Specify typography and color usage

## Critical Anti-Patterns

❌ **Avoid these practices:**
- Overcrowding forms with too many fields
- Inconsistent use of UI patterns across modules
- Poor contrast ratios that harm accessibility
- Ignoring mobile/tablet user experience
- Using non-standard UI elements
- Neglecting error states and edge cases

## Resources & References

- [Odoo 18 UI Guidelines](https://www.odoo.com/documentation/18.0/developer/reference/user_interface.html)
- [OWL Component Design Guide](https://github.com/odoo/owl/blob/master/doc/readme.md)
- [Web Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [Odoo 18 SCSS Framework](https://www.odoo.com/documentation/18.0/developer/reference/frontend/bootstrap.html)