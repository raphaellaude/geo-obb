# geo-obb: Geographic Oriented Bounding Boxes

Lightweight set of utilities (with examples) for calculating oriented bounding boxes on geographic data.

Useful for?

- Quickly assessing parcel dimensions - yes
- Determining the relationship to the street - maybe better? Would be interesting
- For analyzing the rotational correlation of geographic features - yes
- As a measure of compactness - no not really because the OBBs fit so snugly
- As a measure of longness - yes though what this is useful for dunno
- Improving the speed of spatial operations by reducing the false positive rate of rtree comparisons - yes but not worth the computational work to get to that point
- Classifying urban grid networks - yes
  - Which could be useful as a unit of analysis?
  - Or in identifying corridors that split communities?
  - Could look at the local spatial autocorrelation / homogeneity or heterogeneity of obb orientations to identify the "grid-y-ness" of areas as a measure of urban-ness
    - Perhaps this last application could be used to identify areas of development or track development intensity over time
