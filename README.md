# BetterTunes

## Contributers
- Grace Keeney - SE Lead
- Todd Slaughter - Team lead & Security lead
- Brennan Thompson - Testing lead
- Logan Oaks - Coding lead

## Project Overview
The team that developed this app are all students in the UWF Capstone 2025 course. We were given creative freedom for what project we wanted to 
create, as long as it followed the theme of "X, but for Y." We decided to do "GoodReads, but for music" because we know that, as college students,
having good music at the ready is an essential, and we wanted a platform where music lovers could make finding good music a little easier.

### Documentation
- [Doc Repo](https://github.com/UWF-CS-Capston/capstone-project-spring-25-group-4/tree/8105fcf3690e17a759a31246ecf7d5c3110240ee/documentation)

### Demo Links:
- [Demo 1](https://youtu.be/5FnE-yMR11o)
- [Demo 2](https://youtu.be/YMgYpYVsTLE)


### How to Run:

NOTICE: MongoDB is blacklisted on UWF WiFi. Without MongoDB, you won't be able to register a new account or login to an existing one.

1. Install Docker Desktop
   - [Windows x64](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=module)
   - [MAC - Apple Silicon](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=module)
   - [MAC - Intel Chip](https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=module)
2. Cleanup Old Docker Containers
   - Ensure you're in the root of the repo "/capstone-project-spring-25-group-4"
   ```shell
   docker-compose down -v --remove-orphans
   ```
3. Build the Docker Containers
   ```shell
   docker-compose build --no-cache
   ```
4. Start the Docker Containers
   ```shell
   docker-compose up -d
   ```
5. Navigate to the Webpage
   - http://localhost:3000
   
### How to Run (Developer How-To)
1. Setup the Frontend
    - Open a new Terminal Window at the base of the repo ( For example: C:\capstone-project-spring-25-group-4)
    - Navigate to the Frontend Directory
    ``` shell
   cd client
    ```
   - Install requirements for Frontend (using npm).
    ``` shell
   npm install
    ```
   - Start the Frontend
    ``` shell
   npm start
    ```
2. Set up the Backend
   - Open a new Terminal Window at the base of the repo ( For example: C:\capstone-project-spring-25-group-4)
   - Navigate to the Backend directory
    ```shell
    cd server
    ```
   - Initialize a .venv
    ``` shell
    python -m venv .venv
    ```
   - Activate the created .venv
    ```shell
    .\.venv\Scripts\activate
    ```
   -  Install requirements
    ```shell
    pip install -r requirements.txt
    ```
   - Start the Backend
    ```shell
    .\.venv\Scripts\python.exe main.py
    ```
   
