#!/usr/bin/env node
import { greet, whereFrom } from "../lib/greeter.js";

// `hops-greet <name>` on the terminal of an environment that installed this repository as a
// package: the bin link comes from the global install, the module path shows where it landed.
console.log(greet(process.argv[2]));
console.log(`(from ${whereFrom()})`);
