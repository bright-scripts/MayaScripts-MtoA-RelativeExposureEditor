# MtoA Relative Exposure editor

Have you ever thought "Hmm I like this lighting setup but it's all a bit dim / too bright.."
You can change the exposure values of Maya default and Arnold lights by a relative amount so that every light's exposure gets increased/decreased by the same amount.

**By default this option ignores hidden/disabled lights**

## Current options are:

- **Override: Absolute change** -> sets all exposures to given a amount, disregarding current values
- **Selected lights only** -> Only effect selected lights
- **Include hidden lights** -> Effect hidden/disabled lights as well

## Installation

You can drag and drop the `.py` file either:
- into the script editor and run it that way
- or from the script editor (while having it all selected) onto the toolbar to save it there for later use

---

## Notes

- If you'd like to just set absolute values for multiple lights, there's already a built in function for it in the `Arnold` -> `Utilities` -> `Light editor` menu
- This project was mainly just a learning experience, but it might be updated to work with different renderengines used with Maya
