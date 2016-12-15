var Angle, Array, Bool, Color, ContextProperties, Coord, Direction, Distance, Enum, Fill, HasProps, Line, Numeric, Property, String, Text, _, angles, coords, distances, fields, svg_colors, visuals,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty,
  indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

_ = require("underscore");

HasProps = require("./has_props");

svg_colors = require("./svg_colors");

Property = (function(superClass) {
  extend(Property, superClass);

  function Property() {
    return Property.__super__.constructor.apply(this, arguments);
  }

  Property.prototype.initialize = function(attrs, options) {
    Property.__super__.initialize.call(this, attrs, options);
    this.obj = this.get('obj');
    this.attr = this.get('attr');
    this.listenTo(this.obj, "change:" + this.attr, function() {
      this._init();
      return this.obj.trigger("propchange");
    });
    return this._init();
  };

  Property.prototype.serializable_in_document = function() {
    var result;
    if (this.get('obj') != null) {
      result = this.get('obj').serializable_in_document();
      if (!result) {
        console.log("  'obj' field of " + this.constructor.name + " has a nonserializable value of type " + (this.get('obj').constructor.name));
      }
      return result;
    } else {
      return true;
    }
  };

  Property.prototype._init = function() {
    var attr_value;
    attr_value = this.obj.get(this.attr);
    if (_.isObject(attr_value) && !_.isArray(attr_value)) {
      this.spec = attr_value;
      if (!_.isUndefined(this.spec.value)) {
        this.fixed_value = this.spec.value;
      } else if (this.spec.field != null) {
        this.field = this.spec.field;
      } else {
        throw new Error("spec for property '" + attr + "' needs one of 'value' or 'field'");
      }
    } else {
      this.fixed_value = attr_value;
    }
    if ((this.field != null) && !_.isString(this.field)) {
      throw new Error("field value for property '" + attr + "' is not a string");
    }
    if (this.fixed_value != null) {
      return this.validate(this.fixed_value, this.attr);
    }
  };

  Property.prototype.value = function() {
    var result;
    result = this.fixed_value != null ? this.fixed_value : NaN;
    return this.transform([result])[0];
  };

  Property.prototype.array = function(source) {
    var data, i, length, value;
    data = source.get('data');
    if ((this.field != null) && (this.field in data)) {
      return this.transform(source.get_column(this.field));
    } else {
      length = source.get_length();
      if (length == null) {
        length = 1;
      }
      value = this.value();
      return (function() {
        var j, ref, results;
        results = [];
        for (i = j = 0, ref = length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
          results.push(value);
        }
        return results;
      })();
    }
  };

  Property.prototype.transform = function(values) {
    return values;
  };

  Property.prototype.validate = function(value, attr) {
    return true;
  };

  return Property;

})(HasProps);

Numeric = (function(superClass) {
  extend(Numeric, superClass);

  function Numeric() {
    return Numeric.__super__.constructor.apply(this, arguments);
  }

  Numeric.prototype.validate = function(value, attr) {
    if (!_.isNumber(value)) {
      throw new Error("numeric property '" + attr + "' given invalid value: " + value);
    }
    return true;
  };

  Numeric.prototype.transform = function(values) {
    var i, j, ref, result;
    result = new Float64Array(values.length);
    for (i = j = 0, ref = values.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
      result[i] = values[i];
    }
    return result;
  };

  return Numeric;

})(Property);

Angle = (function(superClass) {
  extend(Angle, superClass);

  function Angle() {
    return Angle.__super__.constructor.apply(this, arguments);
  }

  Angle.prototype._init = function() {
    var ref, ref1;
    Angle.__super__._init.call(this);
    this.units = (ref = (ref1 = this.spec) != null ? ref1.units : void 0) != null ? ref : "rad";
    if (this.units !== "deg" && this.units !== "rad") {
      throw new Error("Angle units must be one of 'deg' or 'rad', given invalid value: " + this.units);
    }
  };

  Angle.prototype.transform = function(values) {
    var x;
    if (this.units === "deg") {
      values = (function() {
        var j, len, results;
        results = [];
        for (j = 0, len = values.length; j < len; j++) {
          x = values[j];
          results.push(x * Math.PI / 180.0);
        }
        return results;
      })();
    }
    values = (function() {
      var j, len, results;
      results = [];
      for (j = 0, len = values.length; j < len; j++) {
        x = values[j];
        results.push(-x);
      }
      return results;
    })();
    return Angle.__super__.transform.call(this, values);
  };

  return Angle;

})(Numeric);

Distance = (function(superClass) {
  extend(Distance, superClass);

  function Distance() {
    return Distance.__super__.constructor.apply(this, arguments);
  }

  Distance.prototype._init = function() {
    var ref, ref1;
    Distance.__super__._init.call(this);
    this.units = (ref = (ref1 = this.spec) != null ? ref1.units : void 0) != null ? ref : "data";
    if (this.units !== "data" && this.units !== "screen") {
      throw new Error("Distance units must be one of 'data' or 'screen', given invalid value: " + this.units);
    }
  };

  return Distance;

})(Numeric);

Array = (function(superClass) {
  extend(Array, superClass);

  function Array() {
    return Array.__super__.constructor.apply(this, arguments);
  }

  Array.prototype.validate = function(value, attr) {
    if (!_.isArray(value)) {
      throw new Error("array property '" + attr + "' given invalid value: " + value);
    }
    return true;
  };

  return Array;

})(Property);

Bool = (function(superClass) {
  extend(Bool, superClass);

  function Bool() {
    return Bool.__super__.constructor.apply(this, arguments);
  }

  Bool.prototype.validate = function(value, attr) {
    if (!_.isBoolean(value)) {
      throw new Error("boolean property '" + attr + "' given invalid value: " + value);
    }
    return true;
  };

  return Bool;

})(Property);

Coord = (function(superClass) {
  extend(Coord, superClass);

  function Coord() {
    return Coord.__super__.constructor.apply(this, arguments);
  }

  Coord.prototype.validate = function(value, attr) {
    if (!_.isNumber(value) && !_.isString(value)) {
      throw new Error("coordinate property '" + attr + "' given invalid value: " + value);
    }
    return true;
  };

  return Coord;

})(Property);

Color = (function(superClass) {
  extend(Color, superClass);

  function Color() {
    return Color.__super__.constructor.apply(this, arguments);
  }

  Color.prototype.validate = function(value, attr) {
    if ((svg_colors[value.toLowerCase()] == null) && value.substring(0, 1) !== "#" && !this.valid_rgb(value)) {
      throw new Error("color property '" + attr + "' given invalid value: " + value);
    }
    return true;
  };

  Color.prototype.valid_rgb = function(value) {
    var contents, params, ref, rgb;
    switch (value.substring(0, 4)) {
      case "rgba":
        params = {
          start: "rgba(",
          len: 4,
          alpha: true
        };
        break;
      case "rgb(":
        params = {
          start: "rgb(",
          len: 3,
          alpha: false
        };
        break;
      default:
        return false;
    }
    if (new RegExp(".*?(\\.).*(,)").test(value)) {
      throw new Error("color expects integers for rgb in rgb/rgba tuple, received " + value);
    }
    contents = value.replace(params.start, "").replace(")", "").split(',').map(parseFloat);
    if (contents.length !== params.len) {
      throw new Error("color expects rgba " + expect_len + "-tuple, received " + value);
    }
    if (params.alpha && !((0 <= (ref = contents[3]) && ref <= 1))) {
      throw new Error("color expects rgba 4-tuple to have alpha value between 0 and 1");
    }
    if (indexOf.call((function() {
      var j, len, ref1, results;
      ref1 = contents.slice(0, 3);
      results = [];
      for (j = 0, len = ref1.length; j < len; j++) {
        rgb = ref1[j];
        results.push((0 <= rgb && rgb <= 255));
      }
      return results;
    })(), false) >= 0) {
      throw new Error("color expects rgb to have value between 0 and 255");
    }
    return true;
  };

  return Color;

})(Property);

String = (function(superClass) {
  extend(String, superClass);

  function String() {
    return String.__super__.constructor.apply(this, arguments);
  }

  String.prototype.validate = function(value, attr) {
    if (!_.isString(value)) {
      throw new Error("string property '" + attr + "' given invalid value: " + value);
    }
    return true;
  };

  return String;

})(Property);

Enum = (function(superClass) {
  extend(Enum, superClass);

  function Enum() {
    return Enum.__super__.constructor.apply(this, arguments);
  }

  Enum.prototype.initialize = function(attrs, options) {
    this.levels = attrs.values.split(" ");
    return Enum.__super__.initialize.call(this, attrs, options);
  };

  Enum.prototype.validate = function(value, attr) {
    if (indexOf.call(this.levels, value) < 0) {
      throw new Error("enum property '" + attr + "' given invalid value: " + value + ", valid values are: " + this.levels);
    }
    return true;
  };

  return Enum;

})(Property);

Direction = (function(superClass) {
  extend(Direction, superClass);

  function Direction() {
    return Direction.__super__.constructor.apply(this, arguments);
  }

  Direction.prototype.initialize = function(attrs, options) {
    attrs.values = "anticlock clock";
    return Direction.__super__.initialize.call(this, attrs, options);
  };

  Direction.prototype.transform = function(values) {
    var i, j, ref, result;
    result = new Uint8Array(values.length);
    for (i = j = 0, ref = values.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
      switch (values[i]) {
        case 'clock':
          result[i] = false;
          break;
        case 'anticlock':
          result[i] = true;
      }
    }
    return result;
  };

  return Direction;

})(Enum);

ContextProperties = (function(superClass) {
  extend(ContextProperties, superClass);

  function ContextProperties() {
    return ContextProperties.__super__.constructor.apply(this, arguments);
  }

  ContextProperties.prototype.initialize = function(attrs, options) {
    this.cache = {};
    return ContextProperties.__super__.initialize.call(this, attrs, options);
  };

  ContextProperties.prototype.warm_cache = function(source, attrs) {
    var attr, j, len, prop, results;
    results = [];
    for (j = 0, len = attrs.length; j < len; j++) {
      attr = attrs[j];
      prop = this[attr];
      if (prop.fixed_value != null) {
        results.push(this.cache[attr] = prop.fixed_value);
      } else {
        results.push(this.cache[attr + "_array"] = prop.array(source));
      }
    }
    return results;
  };

  ContextProperties.prototype.cache_select = function(attr, i) {
    var prop;
    prop = this[attr];
    if (prop.fixed_value != null) {
      return this.cache[attr] = prop.fixed_value;
    } else {
      return this.cache[attr] = this.cache[attr + "_array"][i];
    }
  };

  return ContextProperties;

})(HasProps);

Line = (function(superClass) {
  extend(Line, superClass);

  function Line() {
    return Line.__super__.constructor.apply(this, arguments);
  }

  Line.prototype.initialize = function(attrs, options) {
    var obj, prefix;
    Line.__super__.initialize.call(this, attrs, options);
    obj = this.get('obj');
    prefix = this.get('prefix');
    this.color = new Color({
      obj: obj,
      attr: prefix + "line_color"
    });
    this.width = new Numeric({
      obj: obj,
      attr: prefix + "line_width"
    });
    this.alpha = new Numeric({
      obj: obj,
      attr: prefix + "line_alpha"
    });
    this.join = new Enum({
      obj: obj,
      attr: prefix + "line_join",
      values: "miter round bevel"
    });
    this.cap = new Enum({
      obj: obj,
      attr: prefix + "line_cap",
      values: "butt round square"
    });
    this.dash = new Array({
      obj: obj,
      attr: prefix + "line_dash"
    });
    this.dash_offset = new Numeric({
      obj: obj,
      attr: prefix + "line_dash_offset"
    });
    this.do_stroke = true;
    if (!_.isUndefined(this.color.fixed_value)) {
      if (_.isNull(this.color.fixed_value)) {
        return this.do_stroke = false;
      }
    }
  };

  Line.prototype.warm_cache = function(source) {
    return Line.__super__.warm_cache.call(this, source, ["color", "width", "alpha", "join", "cap", "dash", "dash_offset"]);
  };

  Line.prototype.set_value = function(ctx) {
    ctx.strokeStyle = this.color.value();
    ctx.globalAlpha = this.alpha.value();
    ctx.lineWidth = this.width.value();
    ctx.lineJoin = this.join.value();
    ctx.lineCap = this.cap.value();
    ctx.setLineDash(this.dash.value());
    return ctx.setLineDashOffset(this.dash_offset.value());
  };

  Line.prototype.set_vectorize = function(ctx, i) {
    this.cache_select("color", i);
    if (ctx.strokeStyle !== this.cache.fill) {
      ctx.strokeStyle = this.cache.color;
    }
    this.cache_select("alpha", i);
    if (ctx.globalAlpha !== this.cache.alpha) {
      ctx.globalAlpha = this.cache.alpha;
    }
    this.cache_select("width", i);
    if (ctx.lineWidth !== this.cache.width) {
      ctx.lineWidth = this.cache.width;
    }
    this.cache_select("join", i);
    if (ctx.lineJoin !== this.cache.join) {
      ctx.lineJoin = this.cache.join;
    }
    this.cache_select("cap", i);
    if (ctx.lineCap !== this.cache.cap) {
      ctx.lineCap = this.cache.cap;
    }
    this.cache_select("dash", i);
    if (ctx.getLineDash() !== this.cache.dash) {
      ctx.setLineDash(this.cache.dash);
    }
    this.cache_select("dash_offset", i);
    if (ctx.getLineDashOffset() !== this.cache.dash_offset) {
      return ctx.setLineDashOffset(this.cache.dash_offset);
    }
  };

  return Line;

})(ContextProperties);

Fill = (function(superClass) {
  extend(Fill, superClass);

  function Fill() {
    return Fill.__super__.constructor.apply(this, arguments);
  }

  Fill.prototype.initialize = function(attrs, options) {
    var obj, prefix;
    Fill.__super__.initialize.call(this, attrs, options);
    obj = this.get('obj');
    prefix = this.get('prefix');
    this.color = new Color({
      obj: obj,
      attr: prefix + "fill_color"
    });
    this.alpha = new Numeric({
      obj: obj,
      attr: prefix + "fill_alpha"
    });
    this.do_fill = true;
    if (!_.isUndefined(this.color.fixed_value)) {
      if (_.isNull(this.color.fixed_value)) {
        return this.do_fill = false;
      }
    }
  };

  Fill.prototype.warm_cache = function(source) {
    return Fill.__super__.warm_cache.call(this, source, ["color", "alpha"]);
  };

  Fill.prototype.set_value = function(ctx) {
    ctx.fillStyle = this.color.value();
    return ctx.globalAlpha = this.alpha.value();
  };

  Fill.prototype.set_vectorize = function(ctx, i) {
    this.cache_select("color", i);
    if (ctx.fillStyle !== this.cache.fill) {
      ctx.fillStyle = this.cache.color;
    }
    this.cache_select("alpha", i);
    if (ctx.globalAlpha !== this.cache.alpha) {
      return ctx.globalAlpha = this.cache.alpha;
    }
  };

  return Fill;

})(ContextProperties);

Text = (function(superClass) {
  extend(Text, superClass);

  function Text() {
    return Text.__super__.constructor.apply(this, arguments);
  }

  Text.prototype.initialize = function(attrs, options) {
    var obj, prefix;
    Text.__super__.initialize.call(this, attrs, options);
    obj = this.get('obj');
    prefix = this.get('prefix');
    this.font = new String({
      obj: obj,
      attr: prefix + "text_font"
    });
    this.font_size = new String({
      obj: obj,
      attr: prefix + "text_font_size"
    });
    this.font_style = new Enum({
      obj: obj,
      attr: prefix + "text_font_style",
      values: "normal italic bold"
    });
    this.color = new Color({
      obj: obj,
      attr: prefix + "text_color"
    });
    this.alpha = new Numeric({
      obj: obj,
      attr: prefix + "text_alpha"
    });
    this.align = new Enum({
      obj: obj,
      attr: prefix + "text_align",
      values: "left right center"
    });
    return this.baseline = new Enum({
      obj: obj,
      attr: prefix + "text_baseline",
      values: "top middle bottom alphabetic hanging"
    });
  };

  Text.prototype.warm_cache = function(source) {
    return Text.__super__.warm_cache.call(this, source, ["font", "font_size", "font_style", "color", "alpha", "align", "baseline"]);
  };

  Text.prototype.cache_select = function(name, i) {
    var val;
    if (name === "font") {
      val = Text.__super__.cache_select.call(this, "font_style", i) + " " + Text.__super__.cache_select.call(this, "font_size", i) + " " + Text.__super__.cache_select.call(this, "font", i);
      return this.cache.font = val;
    } else {
      return Text.__super__.cache_select.call(this, name, i);
    }
  };

  Text.prototype.font_value = function() {
    var font, font_size, font_style;
    font = this.font.value();
    font_size = this.font_size.value();
    font_style = this.font_style.value();
    return font_style + " " + font_size + " " + font;
  };

  Text.prototype.set_value = function(ctx) {
    ctx.font = this.font_value();
    ctx.fillStyle = this.color.value();
    ctx.globalAlpha = this.alpha.value();
    ctx.textAlign = this.align.value();
    return ctx.textBaseline = this.baseline.value();
  };

  Text.prototype.set_vectorize = function(ctx, i) {
    this.cache_select("font", i);
    if (ctx.font !== this.cache.font) {
      ctx.font = this.cache.font;
    }
    this.cache_select("color", i);
    if (ctx.fillStyle !== this.cache.color) {
      ctx.fillStyle = this.cache.color;
    }
    this.cache_select("alpha", i);
    if (ctx.globalAlpha !== this.cache.alpha) {
      ctx.globalAlpha = this.cache.alpha;
    }
    this.cache_select("align", i);
    if (ctx.textAlign !== this.cache.align) {
      ctx.textAlign = this.cache.align;
    }
    this.cache_select("baseline", i);
    if (ctx.textBaseline !== this.cache.baseline) {
      return ctx.textBaseline = this.cache.baseline;
    }
  };

  return Text;

})(ContextProperties);

angles = function(model, attr) {
  var angle, j, len, ref, result;
  if (attr == null) {
    attr = "angles";
  }
  result = {};
  ref = model[attr];
  for (j = 0, len = ref.length; j < len; j++) {
    angle = ref[j];
    result[angle] = new Angle({
      obj: model,
      attr: angle
    });
  }
  return result;
};

coords = function(model, attr) {
  var j, len, ref, ref1, result, x, y;
  if (attr == null) {
    attr = "coords";
  }
  result = {};
  ref = model[attr];
  for (j = 0, len = ref.length; j < len; j++) {
    ref1 = ref[j], x = ref1[0], y = ref1[1];
    result[x] = new Coord({
      obj: model,
      attr: x
    });
    result[y] = new Coord({
      obj: model,
      attr: y
    });
  }
  return result;
};

distances = function(model, attr) {
  var dist, j, len, ref, result;
  if (attr == null) {
    attr = "distances";
  }
  result = {};
  ref = model[attr];
  for (j = 0, len = ref.length; j < len; j++) {
    dist = ref[j];
    if (dist[0] === "?") {
      dist = dist.slice(1);
      if (model.get(dist) == null) {
        continue;
      }
    }
    result[dist] = new Distance({
      obj: model,
      attr: dist
    });
  }
  return result;
};

fields = function(model, attr) {
  var arg, field, j, len, ref, ref1, result, type;
  if (attr == null) {
    attr = "fields";
  }
  result = {};
  ref = model[attr];
  for (j = 0, len = ref.length; j < len; j++) {
    field = ref[j];
    type = "number";
    if (field.indexOf(":") > -1) {
      ref1 = field.split(":"), field = ref1[0], type = ref1[1], arg = ref1[2];
    }
    if (field[0] === "?") {
      field = field.slice(1);
      if (model.attributes[field] == null) {
        continue;
      }
    }
    switch (type) {
      case "array":
        result[field] = new Array({
          obj: model,
          attr: field
        });
        break;
      case "bool":
        result[field] = new Bool({
          obj: model,
          attr: field
        });
        break;
      case "color":
        result[field] = new Color({
          obj: model,
          attr: field
        });
        break;
      case "direction":
        result[field] = new Direction({
          obj: model,
          attr: field
        });
        break;
      case "enum":
        result[field] = new Enum({
          obj: model,
          attr: field,
          values: arg
        });
        break;
      case "number":
        result[field] = new Numeric({
          obj: model,
          attr: field
        });
        break;
      case "string":
        result[field] = new String({
          obj: model,
          attr: field
        });
    }
  }
  return result;
};

visuals = function(model, attr) {
  var j, len, name, prefix, prop, ref, ref1, result;
  if (attr == null) {
    attr = "visuals";
  }
  result = {};
  ref = model[attr];
  for (j = 0, len = ref.length; j < len; j++) {
    prop = ref[j];
    prefix = "";
    if (prop.indexOf(":") > -1) {
      ref1 = prop.split(":"), prop = ref1[0], prefix = ref1[1];
    }
    name = "" + prefix + prop;
    switch (prop) {
      case "line":
        result[name] = new Line({
          obj: model,
          prefix: prefix
        });
        break;
      case "fill":
        result[name] = new Fill({
          obj: model,
          prefix: prefix
        });
        break;
      case "text":
        result[name] = new Text({
          obj: model,
          prefix: prefix
        });
    }
  }
  return result;
};

module.exports = {
  Angle: Angle,
  Array: Array,
  Bool: Bool,
  Color: Color,
  Coord: Coord,
  Direction: Direction,
  Distance: Distance,
  Enum: Enum,
  Numeric: Numeric,
  Property: Property,
  String: String,
  Line: Line,
  Fill: Fill,
  Text: Text,
  factories: {
    coords: coords,
    distances: distances,
    angles: angles,
    fields: fields,
    visuals: visuals
  }
};
