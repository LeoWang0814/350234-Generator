
# 350234 Expression Builder / 350234 表达式生成器

> 使用一段看似离谱、其实很严谨的动态规划，把任意正整数拆成若干个“3 5 0 2 3 4”之间夹着加减乘除的最短和式。  
> Build the shortest possible sum of expressions, each made from the digits `3 5 0 2 3 4` with `+ - * /` between them, so that the total equals any given positive integer.

---

## 1. What is this? / 这是啥？

This script takes a positive integer `input` and prints an equation like:

```text
你说的可是 3+5*0+2+3+4 + 3*5-0+2+3+4 + ... = input
````

Every term on the left:

1. **Always** comes from the same digit pattern: `3 5 0 2 3 4`
2. **Only** uses the four basic operations: `+ - * /`
3. **Is** guaranteed to evaluate to a **positive integer**
4. And the **entire expression** is a **sum** of those positive-integer “350234 blocks”

What the algorithm guarantees:

* ✅ The final sum **equals** the target integer
* ✅ Every “block” (i.e. one `3 ? 5 ? 0 ? 2 ? 3 ? 4` expression) evaluates to a **positive integer**
* ✅ The set of blocks chosen is **shortest possible** (fewest blocks) for that target
* ✅ Output form is **always**: `block + block + block + ...`
* ✅ Inside each block, the digits are **always** `3 5 0 2 3 4` (this is the meme part)

这个脚本的目标很简单：
给你一个正整数，它会想办法用**若干个**“`3 ? 5 ? 0 ? 2 ? 3 ? 4`”这样的表达式加起来，凑成这个数。
而且它会保证：

* ✅ 每一段都是真的能算出来的正整数
* ✅ 最后一定能凑到你要的那个数
* ✅ 用的段数是**最少的**
* ✅ 每一段里面的数字顺序都是 `350234`
* ✅ 符号只会是 `+ - * /`

---

## 2. Why 350234? / 为什么是 350234？

`350234` 是中文互联网里一个关于“苦命鸳鸯”的梗：爱，死亡和吕奉先。
这里我们把这个梗“算法化”：不只是打印一段梗，而是**真的**用同一串数字反复组合出能算的式子，再用动态规划把它拼成你要的数。

In Chinese meme culture, `350234` is used in a playful, melodramatic way to refer to a pair of “miserable lovers.” The banner in the code is a homage to that. Here, we turn that meme into a **systematic generator** of valid arithmetic expressions — so the output keeps the meme’s shape but actually has mathematical correctness.

---

## 3. How it works / 原理说明

This script is made of **two main phases**.

这个脚本分成**两个阶段**：

### Phase 1: enumerate all valid “350234 blocks”

### 阶段一：枚举所有合法的 “350234 小块”

* We fix the digits: `3 5 0 2 3 4`

* Between 6 numbers there are 5 gaps → each gap can be `+ - * /` → `4^5 = 1024` possibilities

* For each of the 1024 operator combinations, we build an expression like:

  ```text
  3 + 5 * 0 - 2 / 3 + 4
  ```

* Then we `eval(...)` it

* If it

  * does **not** raise `ZeroDivisionError`
  * is **an integer**
  * is **positive**
    we store it in a dictionary:
    **key** = resulting integer value
    **value** = list of expressions that produce exactly this value

In code (`outputVal`):

```python
outputVal[result_value] = [list of different "350234" expressions = result_value]
```

This gives us a **coin set** of positive integers, but each “coin” knows **how to print itself**.

我们先把 `350234` 这串数字中间能塞的 5 个符号全试一遍（`4^5 = 1024` 种），把**能算、是正整数**的那一部分挑出来，按“算出来是多少”分组装进 `outputVal`。
这样我们就得到了一个“面额列表”——但每个面额还自带“怎么写成 350234 表达式”的多种方案。

---

### Phase 2: shortest-sum DP (unbounded knapsack)

### 阶段二：最短和式的动态规划

Now we have a set of positive integers we can produce from a single 350234-expression. The next question is:

> Given these numbers, how do we add them up to get the target with the **fewest terms**?

This is exactly the classic **unbounded knapsack / coin change (min coins)** DP:

```python
dp[i] = minimal number of 350234-blocks to make sum = i
```

* `dp[0] = 0`
* For each available value `num` (i.e. each key in `choices`)
* For each `i` from `num` to `target`:

  * if `dp[i - num] + 1 < dp[i]` then we found a shorter way
  * record that we used `num` to reach `i`

At the end, we backtrack from `target` to 0, so we know exactly **which block values** we used.

由于每一个“350234 小块”都可以用**无限次**，这其实就是**完全背包**里“最少物品数凑出目标值”的版本。
代码里就是这一段：

```python
dp = [float('inf')] * (target + 1)
dp[0] = 0
num_used = [-1] * (target + 1)
...
```

最后再把这些值对应的表达式随机挑一条拼起来，就得到了你看到的那句：

```text
你说的可是 <expr1>+<expr2>+... = <target>
```

---

## 4. Code structure / 代码结构

```text
.
├── generate_expressions  (implicit in top-level for-loop)
│   └── try 1024 operator patterns on "3 5 0 2 3 4"
│       └── collect positive integer results into outputVal
├── solution(...)         # DP: shortest sum using choices
└── main (bottom)         # read target, backtrack, print
```

Key variables / 关键变量：

* `elements = [3,5,0,2,3,4]` 固定数字序列
* `operations = ["+", "-", "*", "/"]` 四则运算
* `outputVal: dict[int, list[str]]`
  同一个结果可能有多种写法 → 随机挑一种
* `choices`
  就是所有能被单次 `350234` 表达式算出来的**正整数集合**，用于 DP
* `solution(choices, target)`
  返回一个列表，里面是你要的那些“面额”（也就是哪些小表达式的值）

---

## 5. Usage / 使用方法

1. **Run the script / 运行脚本**

   ```bash
   python3 main.py
   ```

2. **Input a positive integer / 输入一个正整数**

   ```text
   你可有话说？114
   ```

3. **Program prints expression / 程序输出表达式**

   ```text
   你说的可是3*5-0+2+3*4+3*5-0+2+3*4+3*5+0+2+3*4+3*5-0*2+3*4=114
   ```

Because multiple operator patterns can produce the same number, you may see **different valid outputs** for the same target — this is intended. The value is the same, the representation is randomized.

因为同一个数可能有多种 `350234` 写法，所以**同一个输入你可能看到不一样的输出**，但**都对**，这是故意的。

---

## 6. Guarantees & Constraints / 保证与限制

**Guarantees / 保证：**

* ✅ Every block is based on `3 5 0 2 3 4`
* ✅ Every block evaluates to a **positive integer**
* ✅ Final result is a **sum** of such blocks
* ✅ DP makes the number of blocks **minimal**
* ✅ Final sum equals your input integer

**Current limitations / 当前限制：**

* ❗ Uses Python `eval(...)` — safe enough here but not suited for untrusted input
* ❗ Only works for integers that can actually be composed from the generated block values. In practice with 1024 patterns this covers a **reasonable** range, but not mathematically “all integers forever”
* ❗ Division is integer-like only because we **filter out** non-integer results; so some expressions are simply dropped
* ❗ The operator search space is fixed to 6 digits → 5 gaps → 1024 expressions. If you want **more coverage**, expand this part.

---

## 7. Possible improvements / 可以怎么改

* ✅ **Precompute & cache** the `outputVal` to a JSON / pickle so you don’t enumerate 1024 expressions every time
* ✅ **Add BFS reconstruction** to show not just one shortest answer, but **all** shortest ones
* ✅ **Add CLI options**: e.g. `--show-all-solutions`, `--no-random`
* ✅ **Add unit tests**: for expression generation and DP correctness
* ✅ **Generalize digits**: make `elements = [...]` a parameter instead of hard-coded `350234`

---

## 8. TL;DR / 一句话版

* 先把所有“`3 ? 5 ? 0 ? 2 ? 3 ? 4`”能算成正整数的式子都列出来
* 把它们的结果当成“硬币面额”
* 用动态规划挑**最少数量**的硬币去凑你要的数
* 最后把对应的式子拼起来 → 就得到一条看起来像梗、其实是最优解的表达式

---

## 9. Disclaimer / 声明

This repo/script is for **demonstration and fun with DP + expression enumeration**. The “350234” part is a **cultural meme**; the core algorithm (enumeration + min-coin DP) is general and can be reused with other digit patterns.

本项目只是把一个网络梗工程化一下，核心思想是“表达式枚举 + 最短分解 DP”，完全可以换成别的数字串、别的运算限制。

---
