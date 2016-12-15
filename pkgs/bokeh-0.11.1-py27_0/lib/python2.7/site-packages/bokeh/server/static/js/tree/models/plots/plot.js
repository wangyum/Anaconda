var $, Backbone, Canvas, CartesianFrame, Component, Constraint, ContinuumView, Eq, Expression, Ge, GlyphRenderer, LayoutBox, Le, MIN_BORDER, Operator, Plot, PlotView, Solver, ToolEvents, ToolManager, UIEvents, _, build_views, get_size_for_available_space, global_gl_canvas, kiwi, logger, plot_template, plot_utils, properties,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty,
  indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

_ = require("underscore");

$ = require("jquery");

Backbone = require("backbone");

kiwi = require("kiwi");

Expression = kiwi.Expression, Constraint = kiwi.Constraint, Operator = kiwi.Operator;

Eq = Operator.Eq, Le = Operator.Le, Ge = Operator.Ge;

build_views = require("../../common/build_views");

Canvas = require("../../common/canvas");

CartesianFrame = require("../../common/cartesian_frame");

ContinuumView = require("../../common/continuum_view");

UIEvents = require("../../common/ui_events");

Component = require("../component");

LayoutBox = require("../../common/layout_box");

logger = require("../../common/logging").logger;

plot_utils = require("../../common/plot_utils");

Solver = require("../../common/solver");

ToolManager = require("../../common/tool_manager");

plot_template = require("../../common/plot_template");

properties = require("../../common/properties");

GlyphRenderer = require("../renderers/glyph_renderer");

ToolEvents = require("../../common/tool_events");

global_gl_canvas = null;

MIN_BORDER = 50;

get_size_for_available_space = (function(_this) {
  return function(use_width, use_height, client_width, client_height, aspect_ratio, min_size) {
    var new_height1, new_height2, new_width1, new_width2;
    if (use_width) {
      new_width1 = Math.max(client_width, min_size);
      new_height1 = parseInt(new_width1 / aspect_ratio);
      if (new_height1 < min_size) {
        new_height1 = min_size;
        new_width1 = parseInt(new_height1 * aspect_ratio);
      }
    }
    if (use_height) {
      new_height2 = Math.max(client_height, min_size);
      new_width2 = parseInt(new_height2 * aspect_ratio);
      if (new_width2 < min_size) {
        new_width2 = min_size;
        new_height2 = parseInt(new_width2 / aspect_ratio);
      }
    }
    if ((!use_height) && (!use_width)) {
      return null;
    } else if (use_height && use_width) {
      if (new_width1 < new_width2) {
        return [new_width1, new_height1];
      } else {
        return [new_width2, new_height2];
      }
    } else if (use_height) {
      return [new_width2, new_height2];
    } else {
      return [new_width1, new_height1];
    }
  };
})(this);

PlotView = (function(superClass) {
  extend(PlotView, superClass);

  function PlotView() {
    this.resize_width_height = bind(this.resize_width_height, this);
    this.resize = bind(this.resize, this);
    this.remove = bind(this.remove, this);
    this.request_render = bind(this.request_render, this);
    return PlotView.__super__.constructor.apply(this, arguments);
  }

  PlotView.prototype.className = "bk-plot";

  PlotView.prototype.template = plot_template;

  PlotView.prototype.state = {
    history: [],
    index: -1
  };

  PlotView.prototype.view_options = function() {
    return _.extend({
      plot_model: this.model,
      plot_view: this
    }, this.options);
  };

  PlotView.prototype.pause = function() {
    return this.is_paused = true;
  };

  PlotView.prototype.unpause = function() {
    this.is_paused = false;
    return this.request_render();
  };

  PlotView.prototype.request_render = function() {
    if (!this.is_paused) {
      this.throttled_render(true);
    }
  };

  PlotView.prototype.remove = function() {
    var id, ref, results, tool_view;
    PlotView.__super__.remove.call(this);
    ref = this.tools;
    results = [];
    for (id in ref) {
      tool_view = ref[id];
      results.push(tool_view.remove());
    }
    return results;
  };

  PlotView.prototype.initialize = function(options) {
    var id, j, len, level, ref, ref1, throttled_resize, tool_view, toolbar_location, toolbar_selector;
    PlotView.__super__.initialize.call(this, options);
    this.pause();
    this._initial_state_info = {
      range: null,
      selection: {},
      dimensions: {
        width: this.mget("canvas").get("width"),
        height: this.mget("canvas").get("height")
      }
    };
    this.model.initialize_layout(this.model.solver);
    this.frame = this.mget('frame');
    this.x_range = this.frame.get('x_ranges')['default'];
    this.y_range = this.frame.get('y_ranges')['default'];
    this.xmapper = this.frame.get('x_mappers')['default'];
    this.ymapper = this.frame.get('y_mappers')['default'];
    this.$el.html(this.template());
    this.canvas = this.mget('canvas');
    this.canvas_view = new this.canvas.default_view({
      'model': this.canvas
    });
    this.$('.bk-plot-canvas-wrapper').append(this.canvas_view.el);
    this.canvas_view.render();
    if (this.mget('webgl') || window.location.search.indexOf('webgl=1') > 0) {
      if (window.location.search.indexOf('webgl=0') === -1) {
        this.init_webgl();
      }
    }
    this.throttled_render = plot_utils.throttle_animation(this.render, 15);
    this.outline_props = new properties.Line({
      obj: this.model,
      prefix: 'outline_'
    });
    this.title_props = new properties.Text({
      obj: this.model,
      prefix: 'title_'
    });
    this.background_props = new properties.Fill({
      obj: this.model,
      prefix: 'background_'
    });
    this.border_props = new properties.Fill({
      obj: this.model,
      prefix: 'border_'
    });
    this.renderers = {};
    this.tools = {};
    this.levels = {};
    ref = plot_utils.LEVELS;
    for (j = 0, len = ref.length; j < len; j++) {
      level = ref[j];
      this.levels[level] = {};
    }
    this.build_levels();
    this.bind_bokeh_events();
    this.model.add_constraints(this.canvas.solver);
    this.listenTo(this.canvas.solver, 'layout_update', this.request_render);
    this.ui_event_bus = new UIEvents({
      tool_manager: this.mget('tool_manager'),
      hit_area: this.canvas_view.$el
    });
    ref1 = this.tools;
    for (id in ref1) {
      tool_view = ref1[id];
      this.ui_event_bus.register_tool(tool_view);
    }
    toolbar_location = this.mget('toolbar_location');
    if (toolbar_location != null) {
      toolbar_selector = '.bk-plot-' + toolbar_location;
      logger.debug("attaching toolbar to " + toolbar_selector + " for plot " + this.model.id);
      this.tm_view = new ToolManager.View({
        model: this.mget('tool_manager'),
        el: this.$(toolbar_selector)
      });
    }
    this.update_dataranges();
    if (this.mget('responsive')) {
      throttled_resize = _.throttle(this.resize, 100);
      $(window).on("resize", throttled_resize);
      _.delay(this.resize, 10);
    }
    this.unpause();
    logger.debug("PlotView initialized");
    return this;
  };

  PlotView.prototype.init_webgl = function() {
    var glcanvas, opts;
    glcanvas = global_gl_canvas;
    if (glcanvas == null) {
      global_gl_canvas = glcanvas = document.createElement('canvas');
      opts = {
        'premultipliedAlpha': true
      };
      glcanvas.gl = glcanvas.getContext("webgl", opts) || glcanvas.getContext("experimental-webgl", opts);
    }
    if (glcanvas.gl != null) {
      return this.canvas_view.ctx.glcanvas = glcanvas;
    } else {
      return logger.warn('WebGL is not supported, falling back to 2D canvas.');
    }
  };

  PlotView.prototype.update_dataranges = function() {
    var bds, bounds, follow_enabled, frame, has_bounds, j, k, l, len, len1, len2, len3, m, n, ref, ref1, ref2, ref3, ref4, ref5, v, xr, yr;
    frame = this.model.get('frame');
    bounds = {};
    ref = this.renderers;
    for (k in ref) {
      v = ref[k];
      bds = (ref1 = v.glyph) != null ? typeof ref1.bounds === "function" ? ref1.bounds() : void 0 : void 0;
      if (bds != null) {
        bounds[k] = bds;
      }
    }
    follow_enabled = false;
    has_bounds = false;
    ref2 = _.values(frame.get('x_ranges'));
    for (j = 0, len = ref2.length; j < len; j++) {
      xr = ref2[j];
      if (typeof xr.update === "function") {
        xr.update(bounds, 0, this.model.id);
      }
      if (xr.get('follow') != null) {
        follow_enabled = true;
      }
      if (xr.get('bounds') != null) {
        has_bounds = true;
      }
    }
    ref3 = _.values(frame.get('y_ranges'));
    for (l = 0, len1 = ref3.length; l < len1; l++) {
      yr = ref3[l];
      if (typeof yr.update === "function") {
        yr.update(bounds, 1, this.model.id);
      }
      if (yr.get('follow') != null) {
        follow_enabled = true;
      }
      if (yr.get('bounds') != null) {
        has_bounds = true;
      }
    }
    if (follow_enabled && has_bounds) {
      logger.warn('Follow enabled so bounds are unset.');
      ref4 = _.values(frame.get('x_ranges'));
      for (m = 0, len2 = ref4.length; m < len2; m++) {
        xr = ref4[m];
        xr.set('bounds', null);
      }
      ref5 = _.values(frame.get('y_ranges'));
      for (n = 0, len3 = ref5.length; n < len3; n++) {
        yr = ref5[n];
        yr.set('bounds', null);
      }
    }
    return this.range_update_timestamp = Date.now();
  };

  PlotView.prototype.map_to_screen = function(x, y, x_name, y_name) {
    if (x_name == null) {
      x_name = 'default';
    }
    if (y_name == null) {
      y_name = 'default';
    }
    return this.frame.map_to_screen(x, y, this.canvas, x_name, y_name);
  };

  PlotView.prototype.push_state = function(type, info) {
    var prev_info, ref;
    prev_info = ((ref = this.state.history[this.state.index]) != null ? ref.info : void 0) || {};
    info = _.extend({}, this._initial_state_info, prev_info, info);
    this.state.history.slice(0, this.state.index + 1);
    this.state.history.push({
      type: type,
      info: info
    });
    this.state.index = this.state.history.length - 1;
    return this.trigger("state_changed");
  };

  PlotView.prototype.clear_state = function() {
    this.state = {
      history: [],
      index: -1
    };
    return this.trigger("state_changed");
  };

  PlotView.prototype.can_undo = function() {
    return this.state.index >= 0;
  };

  PlotView.prototype.can_redo = function() {
    return this.state.index < this.state.history.length - 1;
  };

  PlotView.prototype.undo = function() {
    if (this.can_undo()) {
      this.state.index -= 1;
      this._do_state_change(this.state.index);
      return this.trigger("state_changed");
    }
  };

  PlotView.prototype.redo = function() {
    if (this.can_redo()) {
      this.state.index += 1;
      this._do_state_change(this.state.index);
      return this.trigger("state_changed");
    }
  };

  PlotView.prototype._do_state_change = function(index) {
    var info, ref;
    info = ((ref = this.state.history[index]) != null ? ref.info : void 0) || this._initial_state_info;
    if (info.range != null) {
      this.update_range(info.range);
    }
    if (info.selection != null) {
      this.update_selection(info.selection);
    }
    if (info.dimensions != null) {
      return this.update_dimensions(info.dimensions);
    }
  };

  PlotView.prototype.update_dimensions = function(dimensions) {
    return this.canvas._set_dims([dimensions.width, dimensions.height]);
  };

  PlotView.prototype.reset_dimensions = function() {
    return this.update_dimensions({
      width: this.canvas.get('canvas_width'),
      height: this.canvas.get('canvas_height')
    });
  };

  PlotView.prototype.get_selection = function() {
    var j, len, ref, renderer, selected, selection;
    selection = [];
    ref = this.mget('renderers');
    for (j = 0, len = ref.length; j < len; j++) {
      renderer = ref[j];
      if (renderer instanceof GlyphRenderer.Model) {
        selected = renderer.get('data_source').get("selected");
        selection[renderer.id] = selected;
      }
    }
    return selection;
  };

  PlotView.prototype.update_selection = function(selection) {
    var ds, j, len, ref, ref1, renderer, results;
    ref = this.mget("renderers");
    results = [];
    for (j = 0, len = ref.length; j < len; j++) {
      renderer = ref[j];
      if (!(renderer instanceof GlyphRenderer.Model)) {
        continue;
      }
      ds = renderer.get('data_source');
      if (selection != null) {
        if (ref1 = renderer.id, indexOf.call(selection, ref1) >= 0) {
          results.push(ds.set("selected", selection[renderer.id]));
        } else {
          results.push(void 0);
        }
      } else {
        results.push(ds.get('selection_manager').clear());
      }
    }
    return results;
  };

  PlotView.prototype.reset_selection = function() {
    return this.update_selection(null);
  };

  PlotView.prototype._update_single_range = function(rng, range_info, is_panning) {
    var max, min, ref, reversed;
    reversed = rng.get('start') > rng.get('end') ? true : false;
    if (rng.get('bounds') != null) {
      min = rng.get('bounds')[0];
      max = rng.get('bounds')[1];
      if (reversed) {
        if (min != null) {
          if (min >= range_info['end']) {
            range_info['end'] = min;
            if (is_panning != null) {
              range_info['start'] = rng.get('start');
            }
          }
        }
        if (max != null) {
          if (max <= range_info['start']) {
            range_info['start'] = max;
            if (is_panning != null) {
              range_info['end'] = rng.get('end');
            }
          }
        }
      } else {
        if (min != null) {
          if (min >= range_info['start']) {
            range_info['start'] = min;
            if (is_panning != null) {
              range_info['end'] = rng.get('end');
            }
          }
        }
        if (max != null) {
          if (max <= range_info['end']) {
            range_info['end'] = max;
            if (is_panning != null) {
              range_info['start'] = rng.get('start');
            }
          }
        }
      }
    }
    if (rng.get('start') !== range_info['start'] || rng.get('end') !== range_info['end']) {
      rng.have_updated_interactively = true;
      rng.set(range_info);
      return (ref = rng.get('callback')) != null ? ref.execute(rng) : void 0;
    }
  };

  PlotView.prototype.update_range = function(range_info, is_panning) {
    var name, ref, ref1, ref2, ref3, rng;
    this.pause;
    if (range_info == null) {
      ref = this.frame.get('x_ranges');
      for (name in ref) {
        rng = ref[name];
        rng.reset();
      }
      ref1 = this.frame.get('y_ranges');
      for (name in ref1) {
        rng = ref1[name];
        rng.reset();
      }
      this.update_dataranges();
    } else {
      ref2 = this.frame.get('x_ranges');
      for (name in ref2) {
        rng = ref2[name];
        this._update_single_range(rng, range_info.xrs[name], is_panning);
      }
      ref3 = this.frame.get('y_ranges');
      for (name in ref3) {
        rng = ref3[name];
        this._update_single_range(rng, range_info.yrs[name], is_panning);
      }
    }
    return this.unpause();
  };

  PlotView.prototype.reset_range = function() {
    return this.update_range(null);
  };

  PlotView.prototype.build_levels = function() {
    var id_, j, l, len, len1, len2, level, m, old_renderers, renderers_to_remove, t, tools, v, views;
    old_renderers = _.keys(this.renderers);
    views = build_views(this.renderers, this.mget('renderers'), this.view_options());
    renderers_to_remove = _.difference(old_renderers, _.pluck(this.mget('renderers'), 'id'));
    for (j = 0, len = renderers_to_remove.length; j < len; j++) {
      id_ = renderers_to_remove[j];
      delete this.levels.glyph[id_];
    }
    tools = build_views(this.tools, this.mget('tools'), this.view_options());
    for (l = 0, len1 = views.length; l < len1; l++) {
      v = views[l];
      level = v.mget('level');
      this.levels[level][v.model.id] = v;
      v.bind_bokeh_events();
    }
    for (m = 0, len2 = tools.length; m < len2; m++) {
      t = tools[m];
      level = t.mget('level');
      this.levels[level][t.model.id] = t;
      t.bind_bokeh_events();
    }
    return this;
  };

  PlotView.prototype.bind_bokeh_events = function() {
    var name, ref, ref1, rng;
    ref = this.mget('frame').get('x_ranges');
    for (name in ref) {
      rng = ref[name];
      this.listenTo(rng, 'change', this.request_render);
    }
    ref1 = this.mget('frame').get('y_ranges');
    for (name in ref1) {
      rng = ref1[name];
      this.listenTo(rng, 'change', this.request_render);
    }
    this.listenTo(this.model, 'change:renderers', this.build_levels);
    this.listenTo(this.model, 'change:tool', this.build_levels);
    this.listenTo(this.model, 'change', this.request_render);
    return this.listenTo(this.model, 'destroy', (function(_this) {
      return function() {
        return _this.remove();
      };
    })(this));
  };

  PlotView.prototype.set_initial_range = function() {
    var good_vals, name, ref, ref1, rng, xrs, yrs;
    good_vals = true;
    xrs = {};
    ref = this.frame.get('x_ranges');
    for (name in ref) {
      rng = ref[name];
      if ((rng.get('start') == null) || (rng.get('end') == null) || _.isNaN(rng.get('start') + rng.get('end'))) {
        good_vals = false;
        break;
      }
      xrs[name] = {
        start: rng.get('start'),
        end: rng.get('end')
      };
    }
    if (good_vals) {
      yrs = {};
      ref1 = this.frame.get('y_ranges');
      for (name in ref1) {
        rng = ref1[name];
        if ((rng.get('start') == null) || (rng.get('end') == null) || _.isNaN(rng.get('start') + rng.get('end'))) {
          good_vals = false;
          break;
        }
        yrs[name] = {
          start: rng.get('start'),
          end: rng.get('end')
        };
      }
    }
    if (good_vals) {
      this._initial_state_info.range = this.initial_range_info = {
        xrs: xrs,
        yrs: yrs
      };
      return logger.debug("initial ranges set");
    } else {
      return logger.warn('could not set initial ranges');
    }
  };

  PlotView.prototype.render = function(force_canvas) {
    var canvas, ctx, dst_offset, flipped_top, frame, frame_box, gl, height, k, lod_timeout, ref, ref1, src_offset, sx, sy, th, title, trigger, v, vx, vy, width;
    if (force_canvas == null) {
      force_canvas = false;
    }
    logger.trace("Plot.render(force_canvas=" + force_canvas + ")");
    if (Date.now() - this.interactive_timestamp < this.mget('lod_interval')) {
      this.interactive = true;
      lod_timeout = this.mget('lod_timeout');
      setTimeout((function(_this) {
        return function() {
          if (_this.interactive && (Date.now() - _this.interactive_timestamp) > lod_timeout) {
            _this.interactive = false;
          }
          return _this.request_render();
        };
      })(this), lod_timeout);
    } else {
      this.interactive = false;
    }
    width = this.mget("plot_width");
    height = this.mget("plot_height");
    if (this.canvas.get("canvas_width") !== width || this.canvas.get("canvas_height") !== height) {
      this.canvas._set_dims([width, height], trigger = false);
    }
    PlotView.__super__.render.call(this);
    this.canvas_view.render(force_canvas);
    if (this.tm_view != null) {
      this.tm_view.render();
    }
    ctx = this.canvas_view.ctx;
    frame = this.model.get('frame');
    canvas = this.model.get('canvas');
    ref = this.renderers;
    for (k in ref) {
      v = ref[k];
      if (v.model.update_layout != null) {
        v.model.update_layout(v, this.canvas.solver);
      }
    }
    ref1 = this.renderers;
    for (k in ref1) {
      v = ref1[k];
      if ((this.range_update_timestamp == null) || v.set_data_timestamp > this.range_update_timestamp) {
        this.update_dataranges();
        break;
      }
    }
    title = this.mget('title');
    if (title) {
      this.title_props.set_value(this.canvas_view.ctx);
      th = ctx.measureText(this.mget('title')).ascent + this.model.get('title_standoff');
      if (th !== this.model.title_panel.get('height')) {
        this.model.title_panel.set('height', th);
      }
    }
    this.model.get('frame').set('width', canvas.get('width') - 1);
    this.model.get('frame').set('height', canvas.get('height') - 1);
    this.canvas.solver.update_variables(false);
    this.model.get('frame')._update_mappers();
    frame_box = [this.canvas.vx_to_sx(this.frame.get('left')), this.canvas.vy_to_sy(this.frame.get('top')), this.frame.get('width'), this.frame.get('height')];
    this._map_hook(ctx, frame_box);
    this._paint_empty(ctx, frame_box);
    if (ctx.glcanvas) {
      ctx.glcanvas.width = this.canvas_view.canvas[0].width;
      ctx.glcanvas.height = this.canvas_view.canvas[0].height;
      gl = ctx.glcanvas.gl;
      gl.viewport(0, 0, ctx.glcanvas.width, ctx.glcanvas.height);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT || gl.DEPTH_BUFFER_BIT);
      gl.enable(gl.SCISSOR_TEST);
      flipped_top = ctx.glcanvas.height - (frame_box[1] + frame_box[3]);
      gl.scissor(frame_box[0], flipped_top, frame_box[2], frame_box[3]);
      gl.enable(gl.BLEND);
      gl.blendFuncSeparate(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA, gl.ONE_MINUS_DST_ALPHA, gl.ONE);
    }
    if (this.outline_props.do_stroke) {
      this.outline_props.set_value(ctx);
      ctx.strokeRect.apply(ctx, frame_box);
    }
    this._render_levels(ctx, ['image', 'underlay', 'glyph', 'annotation'], frame_box);
    if (ctx.glcanvas) {
      src_offset = 0.5;
      dst_offset = 0.0;
      ctx.drawImage(ctx.glcanvas, src_offset, src_offset, ctx.glcanvas.width, ctx.glcanvas.height, dst_offset, dst_offset, ctx.glcanvas.width, ctx.glcanvas.height);
      logger.debug('drawing with WebGL');
    }
    this._render_levels(ctx, ['overlay', 'tool']);
    if (title) {
      vx = (function() {
        switch (this.title_props.align.value()) {
          case 'left':
            return 0;
          case 'center':
            return this.canvas.get('width') / 2;
          case 'right':
            return this.canvas.get('width');
        }
      }).call(this);
      vy = this.model.title_panel.get('bottom') + this.model.get('title_standoff');
      sx = this.canvas.vx_to_sx(vx);
      sy = this.canvas.vy_to_sy(vy);
      this.title_props.set_value(ctx);
      ctx.fillText(title, sx, sy);
    }
    if (this.initial_range_info == null) {
      return this.set_initial_range();
    }
  };

  PlotView.prototype.resize = function() {
    return this.resize_width_height(true, false);
  };

  PlotView.prototype.resize_width_height = function(use_width, use_height, maintain_ar) {
    var ar, avail_height, avail_width, min_size, w_h;
    if (maintain_ar == null) {
      maintain_ar = true;
    }
    this._re_resized = this._re_resized || 0;
    if (!this.el.parentNode && this._re_resized < 14) {
      setTimeout(((function(_this) {
        return function() {
          return _this.resize_width_height(use_width, use_height, maintain_ar);
        };
      })(this)), Math.pow(2, this._re_resized));
      this._re_resized += 1;
      return;
    }
    avail_width = this.el.clientWidth;
    avail_height = this.el.parentNode.clientHeight - 50;
    min_size = this.mget('min_size');
    if (maintain_ar === false) {
      if (use_width && use_height) {
        return this.canvas._set_dims([Math.max(min_size, avail_width), Math.max(min_size, avail_height)]);
      } else if (use_width) {
        return this.canvas._set_dims([Math.max(min_size, avail_width), this.canvas.get('height')]);
      } else if (use_height) {
        return this.canvas._set_dims([this.canvas.get('width'), Math.max(min_size, avail_height)]);
      }
    } else {
      ar = this.canvas.get('width') / this.canvas.get('height');
      w_h = get_size_for_available_space(use_width, use_height, avail_width, avail_height, ar, min_size);
      if (w_h != null) {
        return this.canvas._set_dims(w_h);
      }
    }
  };

  PlotView.prototype._render_levels = function(ctx, levels, clip_region) {
    var i, indices, j, l, len, len1, len2, level, m, ref, renderer, renderer_view, renderer_views, sortKey;
    ctx.save();
    if (clip_region != null) {
      ctx.beginPath();
      ctx.rect.apply(ctx, clip_region);
      ctx.clip();
      ctx.beginPath();
    }
    indices = {};
    ref = this.mget("renderers");
    for (i = j = 0, len = ref.length; j < len; i = ++j) {
      renderer = ref[i];
      indices[renderer.id] = i;
    }
    sortKey = function(renderer_view) {
      return indices[renderer_view.model.id];
    };
    for (l = 0, len1 = levels.length; l < len1; l++) {
      level = levels[l];
      renderer_views = _.sortBy(_.values(this.levels[level]), sortKey);
      for (m = 0, len2 = renderer_views.length; m < len2; m++) {
        renderer_view = renderer_views[m];
        renderer_view.render();
      }
    }
    return ctx.restore();
  };

  PlotView.prototype._map_hook = function(ctx, frame_box) {};

  PlotView.prototype._paint_empty = function(ctx, frame_box) {
    this.border_props.set_value(ctx);
    ctx.fillRect(0, 0, this.canvas_view.mget('width'), this.canvas_view.mget('height'));
    ctx.clearRect.apply(ctx, frame_box);
    this.background_props.set_value(ctx);
    return ctx.fillRect.apply(ctx, frame_box);
  };

  return PlotView;

})(ContinuumView);

Plot = (function(superClass) {
  extend(Plot, superClass);

  function Plot() {
    return Plot.__super__.constructor.apply(this, arguments);
  }

  Plot.prototype.type = 'Plot';

  Plot.prototype.default_view = PlotView;

  Plot.prototype.initialize = function(attrs, options) {
    var canvas, j, l, len, len1, plots, ref, ref1, ref2, xr, yr;
    Plot.__super__.initialize.call(this, attrs, options);
    ref = _.values(this.get('extra_x_ranges')).concat(this.get('x_range'));
    for (j = 0, len = ref.length; j < len; j++) {
      xr = ref[j];
      xr = this.resolve_ref(xr);
      plots = xr.get('plots');
      if (_.isArray(plots)) {
        plots = plots.concat(this);
        xr.set('plots', plots);
      }
    }
    ref1 = _.values(this.get('extra_y_ranges')).concat(this.get('y_range'));
    for (l = 0, len1 = ref1.length; l < len1; l++) {
      yr = ref1[l];
      yr = this.resolve_ref(yr);
      plots = yr.get('plots');
      if (_.isArray(plots)) {
        plots = plots.concat(this);
        yr.set('plots', plots);
      }
    }
    canvas = new Canvas.Model({
      map: (ref2 = this.use_map) != null ? ref2 : false,
      canvas_width: this.get('plot_width'),
      canvas_height: this.get('plot_height'),
      hidpi: this.get('hidpi'),
      solver: new Solver()
    });
    this.set('canvas', canvas);
    this.solver = canvas.get('solver');
    this.set('tool_manager', new ToolManager.Model({
      tools: this.get('tools'),
      toolbar_location: this.get('toolbar_location'),
      logo: this.get('logo')
    }));
    return logger.debug("Plot initialized");
  };

  Plot.prototype.initialize_layout = function(solver) {
    var canvas, existing_or_new_layout, frame;
    existing_or_new_layout = (function(_this) {
      return function(side, name) {
        var box, j, len, list, model;
        list = _this.get(side);
        box = null;
        for (j = 0, len = list.length; j < len; j++) {
          model = list[j];
          if (model.get('name') === name) {
            box = model;
            break;
          }
        }
        if (box != null) {
          box.set('solver', solver);
        } else {
          box = new LayoutBox.Model({
            name: name,
            solver: solver
          });
          list.push(box);
          _this.set(side, list);
        }
        return box;
      };
    })(this);
    canvas = this.get('canvas');
    frame = new CartesianFrame.Model({
      x_range: this.get('x_range'),
      extra_x_ranges: this.get('extra_x_ranges'),
      x_mapper_type: this.get('x_mapper_type'),
      y_range: this.get('y_range'),
      extra_y_ranges: this.get('extra_y_ranges'),
      y_mapper_type: this.get('y_mapper_type'),
      solver: solver
    });
    this.set('frame', frame);
    this.title_panel = existing_or_new_layout('above', 'title_panel');
    return this.title_panel._anchor = this.title_panel._bottom;
  };

  Plot.prototype.add_constraints = function(solver) {
    var do_side, min_border_bottom, min_border_left, min_border_right, min_border_top;
    min_border_top = this.get('min_border_top');
    min_border_bottom = this.get('min_border_bottom');
    min_border_left = this.get('min_border_left');
    min_border_right = this.get('min_border_right');
    do_side = (function(_this) {
      return function(solver, min_size, side, cnames, dim, op) {
        var box, c0, c1, canvas, elts, frame, j, last, len, padding, r, ref;
        canvas = _this.get('canvas');
        frame = _this.get('frame');
        box = new LayoutBox.Model({
          solver: solver
        });
        c0 = '_' + cnames[0];
        c1 = '_' + cnames[1];
        solver.add_constraint(new Constraint(new Expression(box['_' + dim], -min_size), Ge), kiwi.Strength.strong);
        solver.add_constraint(new Constraint(new Expression(frame[c0], [-1, box[c1]]), Eq));
        solver.add_constraint(new Constraint(new Expression(box[c0], [-1, canvas[c0]]), Eq));
        last = frame;
        elts = _this.get(side);
        for (j = 0, len = elts.length; j < len; j++) {
          r = elts[j];
          if ((ref = r.get('location')) != null ? ref : 'auto' === 'auto') {
            r.set('layout_location', side, {
              silent: true
            });
          } else {
            r.set('layout_location', r.get('location'), {
              silent: true
            });
          }
          if (r.initialize_layout != null) {
            r.initialize_layout(solver);
          }
          solver.add_constraint(new Constraint(new Expression(last[c0], [-1, r[c1]]), Eq), kiwi.Strength.strong);
          last = r;
        }
        padding = new LayoutBox.Model({
          solver: solver
        });
        solver.add_constraint(new Constraint(new Expression(last[c0], [-1, padding[c1]]), Eq), kiwi.Strength.strong);
        return solver.add_constraint(new Constraint(new Expression(padding[c0], [-1, canvas[c0]]), Eq), kiwi.Strength.strong);
      };
    })(this);
    do_side(solver, min_border_top, 'above', ['top', 'bottom'], 'height', Le);
    do_side(solver, min_border_bottom, 'below', ['bottom', 'top'], 'height', Ge);
    do_side(solver, min_border_left, 'left', ['left', 'right'], 'width', Ge);
    return do_side(solver, min_border_right, 'right', ['right', 'left'], 'width', Le);
  };

  Plot.prototype.add_renderers = function(new_renderers) {
    var renderers;
    renderers = this.get('renderers');
    renderers = renderers.concat(new_renderers);
    return this.set('renderers', renderers);
  };

  Plot.prototype.nonserializable_attribute_names = function() {
    return Plot.__super__.nonserializable_attribute_names.call(this).concat(['solver', 'canvas', 'tool_manager', 'frame', 'min_size']);
  };

  Plot.prototype.serializable_attributes = function() {
    var attrs;
    attrs = Plot.__super__.serializable_attributes.call(this);
    if ('renderers' in attrs) {
      attrs['renderers'] = _.filter(attrs['renderers'], function(r) {
        return r.serializable_in_document();
      });
    }
    return attrs;
  };

  Plot.prototype.defaults = function() {
    return _.extend({}, Plot.__super__.defaults.call(this), {
      renderers: [],
      tools: [],
      tool_events: new ToolEvents.Model(),
      h_symmetry: true,
      v_symmetry: false,
      x_mapper_type: 'auto',
      y_mapper_type: 'auto',
      plot_width: 600,
      plot_height: 600,
      title: '',
      above: [],
      below: [],
      left: [],
      right: [],
      toolbar_location: "above",
      logo: "normal",
      lod_factor: 10,
      lod_interval: 300,
      lod_threshold: 2000,
      lod_timeout: 500,
      webgl: false,
      responsive: false,
      min_size: 120,
      hidpi: true,
      title_standoff: 8,
      x_range: null,
      extra_x_ranges: {},
      y_range: null,
      extra_y_ranges: {},
      background_fill_color: "#ffffff",
      background_fill_alpha: 1.0,
      border_fill_color: "#ffffff",
      border_fill_alpha: 1.0,
      min_border: MIN_BORDER,
      min_border_top: MIN_BORDER,
      min_border_left: MIN_BORDER,
      min_border_bottom: MIN_BORDER,
      min_border_right: MIN_BORDER,
      title_text_font: "helvetica",
      title_text_font_size: "20pt",
      title_text_font_style: "normal",
      title_text_color: "#444444",
      title_text_alpha: 1.0,
      title_text_align: "center",
      title_text_baseline: "alphabetic",
      outline_line_color: '#aaaaaa',
      outline_line_width: 1,
      outline_line_alpha: 1.0,
      outline_line_join: 'miter',
      outline_line_cap: 'butt',
      outline_line_dash: [],
      outline_line_dash_offset: 0
    });
  };

  return Plot;

})(Component.Model);

module.exports = {
  get_size_for_available_space: get_size_for_available_space,
  Model: Plot,
  View: PlotView
};
