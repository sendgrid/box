# Installation

Get your [Box Credentials](https://app.box.com/developers/services/edit/)

```bash
mkdir box
cd box
python3 -m venv ~/Workspace/sendgrid/box
source ~/Workspace/sendgrid/box/bin/activate
pip install -r requirements.txt
```

Update credentials in `.env_sample`

```bash
mv .env_sample .env
```

# Execution

```bash
source ~/Workspace/sendgrid/box/bin/activate
source ./.env
python hello_box.py
```