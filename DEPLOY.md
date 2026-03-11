# Deployment Instructions for Render

## Option 1: Using GitHub CLI (if installed)

```bash
# 1. Create a new repository on GitHub (via browser or CLI)
gh repo create customer-segmentation --public

# 2. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/customer-segmentation.git
git push -u origin master
```

## Option 2: Manual Push

```bash
# 1. Create a new repository on GitHub at https://github.com/new
#    Name it "customer-segmentation" and make it public

# 2. Run these commands:
git remote add origin https://github.com/YOUR_USERNAME/customer-segmentation.git
git push -u origin master
```

## Option 3: Using GitHub Desktop

1. Open GitHub Desktop
2. File > Add Local Repository
3. Select the customer-segmentation folder
4. Click "Publish repository"
5. Name it "customer-segmentation"

---

## Deploy to Render

1. Go to https://render.com and sign up with GitHub
2. Click "New +" > "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Name: customer-segmentation
   - Build Command: (leave empty)
   - Start Command: python app.py
5. Click "Create Web Service"

Wait 1-2 minutes for deployment. Your app will be live at `https://customer-segmentation.onrender.com`

---

## Required Files (already prepared)

- `app.py` - Flask application
- `model.py` - RFM segmentation logic
- `templates/index.html` - Frontend UI
- `static/style.css` - Styling
- `requirements.txt` - Dependencies
- `Procfile` - Deployment config

