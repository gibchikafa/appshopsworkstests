import chalk from "chalk";
import { greet } from "../../lib/greeter.js";

console.log(chalk.green(greet(process.argv[2])));
