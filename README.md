# ecommerce-site

## Vision

Our e-commerce website is dedicated to offering a diverse range of Shrek-themed merchandise,
including T-shirts, pants, toys, shoes, socks, and more. The platform is designed to accommodate
two distinct user classes: customers and admins. Admins will benefit from an administrative
dashboard that provides a comprehensive overview of incoming orders, outgoing shipments, and
other essential statistics.
The website will encompass standard e-commerce functionalities, such as a search function, product
filtering, and dedicated product category pages. While ensuring a seamless user experience is
important, our primary focus for this project lies in optimizing the backend infrastructure, aligning
with the assignment’s main priority.

## Tech Stack

Docker | PostgreSQL | Python | Flask | Bootstrap | HTML | CSS | SQLAlchemy
  
# Install and Startup

1. Open the terminal of your choice. (either for your local machine or server instance)


2. Start by cloning the repository to your local machine or server instance.

```
git clone https://github.com/JCG333/ecommerce-site
```

3. Relocate into the project directory **Ecommerce-site** that you've just cloned.

4. Run the following command twice in the terminal. (this will build the docker image and start the containers)

```
docker-compose up --build -d 
```

5. (optional) to ensure functionality, run the following command to make sure all containers are running.

```
docker ps
```

# How to use

The website will (unless instructed otherwise) be exposed to port 4000. (this can be changed in docker files)

## Locally

- Once you've followed the steps in **Install and startup**, go to the following address (http://127.0.0.1:4000/) to reach the website.

## Server

-- Once you've followed the steps in **Install and startup**, the website should appear at the (http://public-ip-of-your-server-instance:4000/).
