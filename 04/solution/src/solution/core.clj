(ns solution.core)

(defn valid [number]
  (let [x (str number)
        r (map (fn [f s] (compare f s)) x (subs x 1))]
        (and (some zero? r) (every? (comp not pos-int?) r))
    )
  )

(defn filter-vals
  [pred m]
  (into {} (filter (fn [[k v]] (pred v))
                    m)))

(defn strict-valid [number]
  (and (true? (valid number))
    (let [x (str number)
        m (apply max-key (comp int key) (filter-vals (fn [v] (<= 2 v)) (frequencies x)))]
      (true? (<= (val m) 2))
      )))

(defn combinations [from to validator]
  (count 
    (filter (fn [x] (validator x))
      (range from to)))
  )

(def from 172930)
(def to 683082)
  
(println "First part" (combinations from to valid))
(println "Second part" (combinations from to strict-valid))
