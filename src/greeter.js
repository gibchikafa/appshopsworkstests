import dayjs from "dayjs";
import startCase from "lodash/startCase.js";

/**
 * A greeting with the time it was made, so a page or a terminal shows that the two dependencies
 * (lodash, dayjs) resolved from the environment and not from a node_modules next to the app.
 */
export function greet(name = "world") {
  return `Hello ${startCase(name)}, it is ${dayjs().format("YYYY-MM-DD HH:mm:ss")}.`;
}

export function whereFrom() {
  return new URL(import.meta.url).pathname;
}
