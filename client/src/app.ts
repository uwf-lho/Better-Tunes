import express, { Application } from "express";
import session from 'express-session';
import { pino } from 'pino';
import flash from "connect-flash";
import path from "path";

import { ErrorMiddleware } from "./middleware/error.middleware";
import { HandlebarsMiddleware } from "./middleware/handlebars.middleware";

import homeRoutes from "./routes/home.routes";
import dashboardRoutes from "./routes/dashboard.routes";
import resultRoutes from "./routes/results.routes";
import aboutRoutes from "./routes/about.routes";
import registerRoutes from "./routes/register.routes";
import loginRouters from "./routes/login.routes";
import reactionRoutes from "./routes/reaction.routes";
import logoutRoutes from "./routes/logout.routes";

class App {
    // Create an instance of express, called "app"
    public app: Application = express();
    public port: number;
    private log: pino.Logger = pino();
  
    // declare Middleware and controller instances
    private errorMiddleware: ErrorMiddleware;
  
    constructor(port: number) {
      // Set up the body parser
      this.app.use(express.urlencoded({ extended: true }));
      this.app.use(express.json());
  
      // Init port
      this.port = port;
  
      // Init the middlware and controllers
      this.errorMiddleware = new ErrorMiddleware();
  
      // set up session
      this.app.use(
          session({
            secret: "your-secret-key",
            resave: false,
            saveUninitialized: false,
          })
        );
  
      // Enable flash messages
      this.app.use(flash());
  
      // Pass session variables to all views
      this.app.use((req, res, next) => {
          res.locals.user = req.session.user || null;
          res.locals.error = req.flash("error");
          res.locals.success = req.flash("success");
          next();
      });
    
  
      // Serve all static resources from the public directory
      this.app.use(express.static(path.join(__dirname, '../../src', 'public')));
      this.app.use('/scripts', express.static(path.join(__dirname, 'scripts')));

      // Set up handlebars for our templating
      HandlebarsMiddleware.setup(this.app);
  
      // Connect the routes from our controllers to express
      this.app.use(homeRoutes);
      this.app.use(dashboardRoutes);
      this.app.use(resultRoutes);
      this.app.use(aboutRoutes);
      this.app.use(registerRoutes);
      this.app.use(loginRouters);
      this.app.use(reactionRoutes);
      this.app.use(logoutRoutes);
  
      // Error handling middleware (typically set after routes)
      this.app.use(this.errorMiddleware.router);
    }
  
    public listen() {
      // Tell express to start listening for requests on the port we specified
      this.app.listen(this.port, () => {
        this.log.info(
          `Express started on http://localhost:${this.port}; press Ctrl-C to terminate.`
        );
      });
    }
  }
  
  export default App;