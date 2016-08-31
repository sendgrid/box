# Demo Sending Email with Attachment Stored in Box

## Installation

Get your [SendGrid Account](https://app.sendgrid.com/signup?source=boxdev)

Get your [Box Credentials](https://app.box.com/developers/services/edit/)

```bash
git clone https://github.com/sendgrid/box.git
cd box
python3 -m venv .
source ./bin/activate
pip install -r requirements.txt
```

Update credentials in `.env_sample`.

```bash
mv .env_sample .env
```

## Execution

Update configuration variables in [send_demo.py](https://github.com/sendgrid/box/blob/master/send_demo.py#L16).

```bash
source ./bin/activate
source ./.env
python send_demo.py
```