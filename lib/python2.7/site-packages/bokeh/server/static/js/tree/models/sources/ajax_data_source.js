var $, AjaxDataSource, RemoteDataSource, _, logger,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

$ = require("jquery");

_ = require("underscore");

logger = require("../../common/logging").logger;

RemoteDataSource = require("./remote_data_source");

AjaxDataSource = (function(superClass) {
  extend(AjaxDataSource, superClass);

  function AjaxDataSource() {
    this.defaults = bind(this.defaults, this);
    this.get_data = bind(this.get_data, this);
    this.setup = bind(this.setup, this);
    this.destroy = bind(this.destroy, this);
    return AjaxDataSource.__super__.constructor.apply(this, arguments);
  }

  AjaxDataSource.prototype.type = 'AjaxDataSource';

  AjaxDataSource.prototype.destroy = function() {
    if (this.interval != null) {
      return clearInterval(this.interval);
    }
  };

  AjaxDataSource.prototype.setup = function(plot_view, glyph) {
    this.pv = plot_view;
    this.get_data(this.get('mode'));
    if (this.get('polling_interval')) {
      return this.interval = setInterval(this.get_data, this.get('polling_interval'), this.get('mode'), this.get('max_size'), this.get('if_modified'));
    }
  };

  AjaxDataSource.prototype.get_data = function(mode, max_size, if_modified) {
    if (max_size == null) {
      max_size = 0;
    }
    if (if_modified == null) {
      if_modified = false;
    }
    $.ajax({
      dataType: 'json',
      ifModified: if_modified,
      url: this.get('data_url'),
      xhrField: {
        withCredentials: true
      },
      method: this.get('method'),
      contentType: this.get('content_type'),
      headers: this.get('http_headers')
    }).done((function(_this) {
      return function(data) {
        var column, i, len, original_data, ref;
        if (mode === 'replace') {
          _this.set('data', data);
        } else if (mode === 'append') {
          original_data = _this.get('data');
          ref = _this.columns();
          for (i = 0, len = ref.length; i < len; i++) {
            column = ref[i];
            data[column] = original_data[column].concat(data[column]).slice(-max_size);
          }
          _this.set('data', data);
        } else {
          logger.error("unsupported mode: " + mode);
        }
        logger.trace(data);
        return null;
      };
    })(this)).error(function() {
      return logger.error(arguments);
    });
    return null;
  };

  AjaxDataSource.prototype.defaults = function() {
    return _.extend({}, AjaxDataSource.__super__.defaults.call(this), {
      mode: 'replace',
      data_url: null,
      content_type: 'application/json',
      http_headers: {},
      max_size: null,
      method: 'POST',
      if_modified: false
    });
  };

  return AjaxDataSource;

})(RemoteDataSource.Model);

module.exports = {
  Model: AjaxDataSource
};
