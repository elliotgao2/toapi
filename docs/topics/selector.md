Selector fields is used to parse field values from HTML. There are three selectors right now:

- XPath
- Css
- Regex

## Core arguments

Each Selector field class constructor takes at least these arguments.  Some Field classes take additional, field-specific arguments, but the following should always be accepted:

### `rule`

The arguments `rule` is the rule of selector which maybe a xpath expression or a css select expression or a regex expression.
 
## XPath Selector

The rule argument is xpath expression.

```python
from toapi import XPath

field = XPath('//a[@class="user"]/text()')
```

**Signature:** `XPath(rule)`

---

## Css Selector

The rule argument is css select expression.

```python
from toapi import Css

field = Css('a.user', attr='href')
```

**Signature:** `Css(rule, attr=None)`

- `attr` Css select expression can't determine which part ot parse. We need the `attr` argument for that.

---

## Regex Selector

The rule argument regex expression.

```python
from toapi import Regex

field = Regex('\d{18}')
```

**Signature:** `Regex(rule)`

---