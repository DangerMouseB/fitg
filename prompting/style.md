Casing Conventions:
- private names begin with an underscore (_)
- function names - camelCase
- variable names - camelCase
- class names - PascalCase
- database tables - PascalCase
- file names - snake_case
- constants - UPPER_SNAKE_CASE


principles:
- prioritize readability
- reduce phoneme / syllable count without sacrificing clarity


line spacing:
- vertical space is a premium so try to format code compactly
- use short but clear names for variables of lesser importance
  - to reduce need for comments
  - make code more compact and easier to read
- use longer, more descriptive names for variables of greater importance
  - to reduce need for comments
- put simple comments at the end of lines where possible to save vertical space
- production code
  - don't write production code in blog / tutorial style with excessive vertical spacing
  - avoid explanatory comments that would be obvious to a competent reader but useful for a beginner
- simple phrases in if statements can be placed on the same line to save vertical space
  - e.g. if isValid: return True
- simple assigments can be placed on the same line to save vertical space
  - bids, asks = [], []
- use 2 and 3 blank lines to demark major sections of code
  - e.g. between class definitions
  - e.g. between major sections of a long function
- use a single blank line to separate minor sections of code
  - e.g. between method definitions within a class
  - e.g. between logical sections of code within a function
- when using 2–3 blank lines for major sections, actively remove single blank lines that don't add structure
  - avoid "floating" blank lines between a comment and the code it refers to
  - avoid blank lines inside a tight if/elif protocol handler unless they separate phases (validate / update / reply)
  - phase headers (e.g. "# update provider quotes") stick to surrounding code
    - no blank line immediately before the phase header
    - no blank line after a guard/setup line if the next line is the phase header
- section titles (major headings like "# LIFECYCLE", "# MESSAGE HANDLERS")
  - use 2 blank lines before the title
  - use 1 blank line after the title
  - use the title instead of extra single blank lines inside the section


# human parsing (subjective, but keep the visual language consistent)
- give blank lines a semantic meaning (like punctuation)
  - 0 blank lines: same thought / same phase
  - 1 blank line: minor topic shift within the same handler/function
  - 2–3 blank lines: major boundary (new concept / new protocol section / new class)
- one separator per boundary
  - use either a header comment or a blank-line gap as the primary separator (not both)
  - if you do use a header comment for a boundary, prefer removing adjacent single blank lines unless you are intentionally using 2–3 blank lines
- in long protocol handlers (msgArrived), prefer a small number of repeated phases (guard/setup → update state → reply/broadcast)
  - allow at most one blank line between phases; avoid blank lines inside a phase


Naming Conventions:
- dictionary / mapping keyed by XXX with contents YYY
    - preferred style is YYYByXXX, e.g. addrByProviderName, emailByUserId
    - alternative style is XXXToYYYMap, e.g. providerNameToAddrMap, userIdToEmailMap
- datetime type
    - suffix with DT, e.g. startDT
- identity - string or numeric
    - suffix with Id, e.g. userId
- textual name
    - suffix with Name, e.g. userName, assetName
- list / array / tuple / set of XXX
    - suffix with "s", e.g. userIds, assetNames, errorMessages
- prefer short "obvious from context" names for minor intermediate values
  - e.g. addr, msg, ok, i
  - especially for local temporaries returned from lookups / pops where the meaning is clear from the container/key
    - e.g. addr = addrByProviderName.pop(providerName, None)
  - avoid longer "derived" names (e.g. removedAddr) unless it materially improves clarity


Common names:
- conn - a vlmessaging.Connection object
- i, j, k - loop indices
- fn - function
- dt - datetime.datetime object
- d - datetime.date object
- msg - a vlmessaging.Message object
- reply - a vlmessaging.Message object that is a reply to another message
- after - datetime.datetime, datetime.timedelta or milliseconds integer


Unit conventions:
- time intervals in milliseconds unless otherwise specified
- percentages as decimals, e.g. 2% is 0.02


Comments:
- use OPEN: 
  - as a prefix for comments indicating incomplete work or known issues


Software Development Life Cycle - SDLC:
we wish to make as much progress as possible with minimal code
- prefer clear working solutions that make the happy path work
- do the simplest possible thing that could possibly work


Gotchas:
- using dict.get
  - always provide a default value preferring the sentinel Missing
  - e.g. addr = addrByProviderName.get(providerName, Missing) and never addr = addrByProviderName.get(providerName)
- default arguments
  - use the sentinel Missing
  - e.g. def fn(param=Missing): if param is Missing: param = []


Type hints:
- use the minimal amount of type hinting necessary to make code clear and maintainable especially by an AI
- after an API is established and stable, add type hints to the API surface
- avoid excessive type hints on internal implementation details unless they materially improve clarity and maintainability
- prefer descriptive names to excessive type hints
