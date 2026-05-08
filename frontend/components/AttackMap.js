import {
  ComposableMap,
  Geographies,
  Geography,
  Marker
} from "react-simple-maps";

export default function AttackMap() {

  const attacks = [
    { name: "India", coordinates: [78.9629, 20.5937] },
    { name: "Russia", coordinates: [105.3188, 61.5240] },
  ];

  return (
    <ComposableMap>

      <Geographies geography=
        "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json"
      >

        {({ geographies }) =>
          geographies.map((geo) => (
            <Geography
              key={geo.rsmKey}
              geography={geo}
            />
          ))
        }

      </Geographies>

      {attacks.map(({ name, coordinates }) => (
        <Marker key={name} coordinates={coordinates}>
          <circle r={5} fill="red" />
        </Marker>
      ))}

    </ComposableMap>
  );
}