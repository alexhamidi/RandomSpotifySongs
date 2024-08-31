# Spotibulk

## Info

- Supports fetching a very high number of spotify song ids (tested to 2 million, though it took a while)
- Uses a Breath-first search approach on artists' related artists to gradually expand the search space
- Provides several parameters to adjust the search behavior, allowing you to fine-tune the app based on your needs (See usage for details)
- The primary script can be easily modified to fetch albums or artists


## Usage

```js
import chalk from 'chalk';

console.log(chalk.blue('Hello world!'));
```
