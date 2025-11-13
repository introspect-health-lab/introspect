# Logo Setup Instructions

## 📸 Adding the Introspect Logo

The Introspect logo has been integrated into the web interface. Follow these steps to add the logo image file:

### 1. Save the Logo Image

Save your logo image file as:
```
src/frontend/static/images/introspect-logo.png
```

### 2. Logo Specifications

For best results, use:
- **Format**: PNG with transparent background
- **Dimensions**: 400-600px width recommended
- **Background**: White background works well (as mentioned)
- **File size**: Keep under 200KB for fast loading

### 3. Logo Usage in Templates

The logo is already integrated in the following pages:
- **Landing Page** (`index.html`) - Large logo in hero section
- **Sign In Page** (`signin.html`) - Medium logo at top
- **Sign Up Page** (`signup.html`) - Medium logo at top

### 4. Verify Logo Display

After adding the logo file:

1. Start the application:
   ```bash
   uvicorn src.main:app --reload
   ```

2. Open browser and navigate to:
   - `http://localhost:8000/` - Check landing page
   - `http://localhost:8000/signin` - Check sign in page
   - `http://localhost:8000/signup` - Check sign up page

3. The logo should display automatically

### 5. Troubleshooting

If logo doesn't appear:

**Check file path:**
```bash
ls -la src/frontend/static/images/introspect-logo.png
```

**Check file permissions:**
```bash
chmod 644 src/frontend/static/images/introspect-logo.png
```

**Clear browser cache:**
- Press `Ctrl+Shift+R` (Windows/Linux)
- Press `Cmd+Shift+R` (Mac)

**Check browser console:**
- Press `F12` to open developer tools
- Look for 404 errors in Console tab

### 6. Alternative: Use Base64 Encoding

If you prefer to embed the logo directly in HTML:

```bash
# Convert logo to base64
base64 introspect-logo.png > logo-base64.txt
```

Then update templates to use:
```html
<img src="data:image/png;base64,<paste-base64-here>" alt="Introspect Logo">
```

### 7. Customization

To adjust logo size in different pages, edit the CSS classes:

**Landing page** (`index.html` line 11):
```html
<img src="/static/images/introspect-logo.png" alt="Introspect Logo" class="h-20">
```
Change `h-20` to `h-16`, `h-24`, etc.

**Sign in/Sign up pages** (`signin.html`, `signup.html`):
```html
<img src="/static/images/introspect-logo.png" alt="Introspect Logo" class="h-16 mx-auto">
```

### 8. Adding Logo to Dashboard

To add the logo to the dashboard navigation, edit `src/frontend/templates/dashboard.html`:

```html
<div class="flex items-center">
    <img src="/static/images/introspect-logo.png" alt="Introspect" class="h-8 mr-3">
    <span class="text-xl font-bold">Introspect</span>
</div>
```

## 🎨 Logo Design Notes

Based on the provided logo:
- **Eye symbol**: Represents vision and insight (introspection)
- **Blue color scheme**: Professional, trustworthy, medical
- **Clean design**: Modern and accessible

The logo works well with:
- White backgrounds (as mentioned)
- Light gray backgrounds (`bg-gray-50`)
- Gradient backgrounds (cyan to blue)

## 📝 Next Steps

1. Save your logo file to `src/frontend/static/images/introspect-logo.png`
2. Restart the application
3. Verify logo appears on all pages
4. Adjust sizing if needed

## 🔄 Future Enhancements

Consider adding:
- Favicon (16x16, 32x32 versions)
- Apple touch icon (180x180)
- Social media preview image (1200x630)
- Print-friendly version

## 📞 Support

If you encounter issues with logo display, check:
- File path is correct
- File permissions are readable
- Static files are being served correctly
- Browser cache is cleared

