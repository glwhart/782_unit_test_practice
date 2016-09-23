# Revision History

## Revision 0.0.1

- Added unit tests, setup CI, etc.

##

- Fixed some unit tests, checked coverage
- Fixed bug in __getattr__ in Potential class: replaced "self.params" with
  with "self.params[attr]  (Duh!)
