# Foxy and Fawnie in the henhouse


## Usage example of the client:
Startup and login:
<img width="1919" height="709" alt="Screenshot 2026-11-09 130633" src="https://github.com/user-attachments/assets/b409d87d-eabe-48e1-bfd1-f1230a40ddc5" />

Help command:
<img width="1919" height="407" alt="Screenshot 2026-11-09 125331" src="https://github.com/user-attachments/assets/82de7d48-b946-4bde-b8c8-bd419b1459ae" />

List modules:
<img width="1919" height="445" alt="Screenshot 2026-11-09 134737" src="https://github.com/user-attachments/assets/2d71c87d-7d46-455d-a375-bfa75135079b" />

List available chickens:
<img width="1919" height="253" alt="Screenshot 2026-11-09 125819" src="https://github.com/user-attachments/assets/4e214d76-ec9a-483d-b86c-cf14524a889c" />

Interact with a chicken:
<img width="1919" height="216" alt="Screenshot 2026-11-09 130035" src="https://github.com/user-attachments/assets/a1dd5271-e60d-426b-89ed-acb9b039e90f" />

Download file from victim machine:
<img width="1919" height="327" alt="Screenshot 2026-11-09 130949" src="https://github.com/user-attachments/assets/775a32cc-bb94-4c8c-9e1e-f3965027c4fe" />

Upload malicius code on victim machine:
<img width="1919" height="192" alt="Screenshot 2026-11-09 132201" src="https://github.com/user-attachments/assets/8a2ca993-f181-4fa6-b99e-e52b53c14bff" />

Execute UAC bypass module:
<img width="1919" height="474" alt="Screenshot 2026-11-09 134006" src="https://github.com/user-attachments/assets/5f4653fa-55a9-405a-825f-bf9278f283a0" />
<img width="1919" height="72" alt="Screenshot 2026-11-09 134059" src="https://github.com/user-attachments/assets/5672cf0d-d197-4522-a379-bd711dd8bb87" />



## Setup of the server:
Start the server:
```bash
python Henhouse.py
```

Credentials can be found in Data/creds.json and can be crafted like this:
```JSON
{
  "[username]":"[MD5 HASH]",
  "fawnie":"d8578edf8458ce06fbc5bb76a58c5ca4"
}
```

