var Bokeh, logging;

Bokeh = {};

Bokeh.require = require;

Bokeh.version = '0.11.1';

Bokeh._ = require("underscore");

Bokeh.$ = require("jquery");

Bokeh.Backbone = require("backbone");

Bokeh.Backbone.$ = Bokeh.$;

logging = require("./common/logging");

Bokeh.logger = logging.logger;

Bokeh.set_log_level = logging.set_log_level;

if (!window.Float64Array) {
  Bokeh.logger.warn("Float64Array is not supported. Using generic Array instead.");
  window.Float64Array = Array;
}

Bokeh.index = require("./common/base").index;

Bokeh.embed = require("./common/embed");

Bokeh.Collections = require("./common/base").Collections;

Bokeh.Config = require("./common/base").Config;

Bokeh.Bokeh = Bokeh;

module.exports = Bokeh;
