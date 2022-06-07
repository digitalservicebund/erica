# Steuerlotse Erica service
🇬🇧
Erica is a service to send tax declarations to ELSTER. 
It is a wrapper around the functionality of EriC, ELSTER's own client to access their APIs.
It provides functionality to send tax declarations, as well as request, activate and revoke unlock codes.

It was originally [developed as part of the Tech4Germany Fellowship 2020](https://github.com/tech4germany/steuerlotse). 
The fellowship is organized by [DigitalService GmbH des Bundes](https://digitalservice4germany.com).

🇩🇪
Erica ist ein Service, um Steuererklärungen an ELSTER zu senden.
Es dient als Wrapper um die Funktionalität von EriC, ELSTERs eigener Client um die APIs zu verwenden.
Es stellt Funktionalität zum Absenden von Steuererklärungen sowie dem Beantragen, Freischalten und Stornieren von Freischaltcodes bereit.

Ursprünglich wurde es [als Teil des Tech4Germany Fellowships 2020 entwickelt](https://github.com/tech4germany/steuerlotse), 
das von der [DigitalService GmbH des Bundes](https://digitalservice4germany.com) organisiert wird.

# Contributing

🇬🇧
Everyone is welcome to contribute the development of the _Steuerlotse_. You can contribute by opening pull request, 
providing documentation or answering questions or giving feedback. Please always follow the guidelines and our 
[Code of Conduct](CODE_OF_CONDUCT.md).

🇩🇪  
Jede:r ist herzlich eingeladen, die Entwicklung der _Steuerlotse_ mitzugestalten. Du kannst einen Beitrag leisten, 
indem du Pull-Requests eröffnest, die Dokumentation erweiterst, Fragen beantwortest oder Feedback gibst. 
Bitte befolge immer die Richtlinien und unseren [Verhaltenskodex](CODE_OF_CONDUCT_DE.md). 

## Contributing code
🇬🇧 
Open a pull request with your changes and it will be reviewed by someone from the team. When you submit a pull request, 
you declare that you have the right to license your contribution to the DigitalService and the community. 
By submitting the patch, you agree that your contributions are licensed under the MIT license.

Please make sure that your changes have been tested befor submitting a pull request.

🇩🇪  
Nach dem Erstellen eines Pull Requests wird dieser von einer Person aus dem Team überprüft. Wenn du einen Pull-Request 
einreichst, erklärst du dich damit einverstanden, deinen Beitrag an den DigitalService und die Community zu 
lizenzieren. Durch das Einreichen des Patches erklärst du dich damit einverstanden, dass deine Beiträge unter der 
MIT-Lizenz lizenziert sind.

Bitte stelle sicher, dass deine Änderungen getestet wurden, bevor du einen Pull-Request sendest.

# For Developers 👩‍💻 👨‍💻

## Prerequisites

The following prerequisites must be installed:

- python 3.9
- pipenv
- postgresql client >9.1
- docker and docker-dompose

## Getting started 🛠

### Install Python dependencies

```bash
pipenv install
```

### Download ERiC

Erica uses Pyeric, which is a wrapper around ERiC. For this to work you will need to download the latest ERiC 
library and place the required library files in a `lib` folder.

 - Set the environment variable `ERICA_ENV` to `testing`, `development` or similar.
 - Download `ERiC-35.2.8.0-Linux-x86_64.jar` (or a newer version) from the [ELSTER developer portal](https://www.elster.de/elsterweb/infoseite/entwickler).
 - Unpack the downloaded jar file
 - Copy the following library files into `erica/erica_legacy/lib` such that it matches the given structure:

```bash
pyeric$ tree lib
lib
├── libericapi.so
├── libericxerces.so
├── libeSigner.so
└── plugins2
    ├── libcheckElsterDatenabholung.so
    ├── libcheckESt_2021.so
    ├── libcheckVaSt.so
    └── libcommonData.so
```

_NOTE_: If you use a Mac, get the corresponding `*.dylib` files

### Obtain Certificate

You also need to obtain a test certificate from ELSTER and place it under `erica/erica_legacy/instances/blueprint/cert.pfx`.

## Developing 👩‍💻 👨‍💻

### Start your docker:
```bash
docker-compose up
```

### Run Alembic migration on database:
```
env ERICA_ENV=development SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost/db alembic upgrade head
```

### Start the erica API:
```bash
pipenv shell
export ERICA_ENV=development
python3 -m erica
```
Note: Swagger UI will be available under: http://localhost:8000/docs 

### Start a worker:
```bash
pipenv shell
python3 -m erica.infrastructure.rq.worker [dongle|cert|common]
```

## Testing 📃

You can run tests as follows:
```bash
pipenv run pytest
```

If you are missing the ERiC library or a suitable certificate then the respective 
tests will be skipped.
