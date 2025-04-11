// Import the express and handlebars libraries
import { Application } from "express";
import { engine } from "express-handlebars";

export const HandlebarsMiddleware = {
  setup(app: Application) {
    // set up handlebars view engine, register w/ express
    app.engine(
      ".hbs",
      engine({
        extname: ".hbs",
        defaultLayout: "main",
        helpers: {
          eq: function (a: any, b: any) {
            return a === b;
          }
        }
      })
    );
    app.set("view engine", ".hbs");
    app.set("views", "./src/views");
  },
};