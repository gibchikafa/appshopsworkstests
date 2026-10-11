import chalk from "chalk";
import { greet } from "../../src/greeter.js";

console.log(chalk.green(greet(process.argv[2])));
