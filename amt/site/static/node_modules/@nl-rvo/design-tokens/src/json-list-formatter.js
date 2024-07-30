/**
 * @license EUPL-1.2
 * Copyright (c) 2021 Robbert Broersma
 */
module.exports = {
  'json/list': function ({ dictionary }) {
    return JSON.stringify(dictionary.allTokens, null, '  ');
  },
};
