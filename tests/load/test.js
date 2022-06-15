import http from "k6/http";
import { check, fail, group, sleep } from "k6";
import { Rate, Trend } from "k6/metrics";

export const errorRate = new Rate("errors");
export const jobCompletionTime = new Trend("erica_job_duration", true);

export let options = {
  scenarios: {
    default: {
      executor: "ramping-arrival-rate",
      startRate: 5,
      timeUnit: "1m",
      preAllocatedVUs: 1,
      maxVUs: 50,
      stages: [
        { target: 5, duration: "1m" }, // normal submissions
        { target: 10, duration: "15s" },
        { target: 10, duration: "2m" }, // peak submissions or normal registrations (guesstimate for FSC request numbers)
        { target: 40, duration: '15s' },
        { target: 40, duration: '2m' }, // peak submissions + registrations
        // { target: 90, duration: '15s' },
        // { target: 90, duration: '2m' }, // stress
        { target: 5, duration: "15s" },
        { target: 5, duration: "1m" }, // return to normal
      ],
    },
  },
  thresholds: {
    errors: ["rate<0.02"], // 2% max error rate
    erica_job_duration: ["p(95)<120000"], // p95 < 2minutes
  },
};

const MAX_PROCESSING_TIME = 5 * 60 * 1000; // 5 minutes
const WAIT_TIME_BETWEEN_REQUESTS = 0.5;
const baseUrl = "http://erica-api.erica-staging/";
const submitUrl = `${baseUrl}v2/grundsteuer`;

function abort(msg) {
  errorRate.add(1);
  fail(msg);
}

export default function () {
  const params = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  let startTime = Date.now();
  let statusUrl;

  group("submit job", function () {
    let response = http.post(submitUrl, JSON.stringify(jobData), params);
    check(
      response,
      {
        "status is 201": (r) => r.status == 201,
      },
      ["submit"]
    ) || abort(response.status);
    statusUrl = response.headers.Location;
  });

  sleep(WAIT_TIME_BETWEEN_REQUESTS);

  group("poll status", function () {
    while (true) {
      if (Date.now() - startTime > MAX_PROCESSING_TIME) {
        abort("MAX_PROCESSING_TIME exceeded");
        break;
      }

      let response = http.get(`${baseUrl}${statusUrl}`);
      check(
        response,
        {
          "status is 200": (r) => r.status == 200,
        },
        ["poll-status"]
      ) || abort(response.status);

      const responseData = response.json();
      const status = responseData.processStatus;
      if (status === "Processing") {
        sleep(WAIT_TIME_BETWEEN_REQUESTS);
      } else if (status === "Success") {
        errorRate.add(0);
        jobCompletionTime.add(Date.now() - startTime);
        break;
      } else {
        // Failure
        jobCompletionTime.add(Date.now() - startTime);
        abort(
          `Processing failed: ${responseData.errorCode} - ${responseData.errorMessage}`
        );
        break;
      }
    }
  });
}

const jobData = {
  payload: {
    grundstueck: {
      typ: "einfamilienhaus",
      adresse: {
        strasse: "GST Strasse",
        hausnummer: "2",
        hausnummerzusatz: "GST",
        zusatzangaben: "GST Zusatzangaben",
        plz: "12345",
        ort: "GST Ort",
        bundesland: "BB",
      },
      steuernummer: "09841275756757579",
      innerhalbEinerGemeinde: "true",
      bodenrichtwert: "123,00",
      flurstueck: [
        {
          angaben: {
            grundbuchblattnummer: "1",
            gemarkung: "2",
          },
          flur: {
            flur: "1",
            flurstueckZaehler: "23",
            flurstueckNenner: "45",
            wirtschaftlicheEinheitZaehler: "67.1000",
            wirtschaftlicheEinheitNenner: "89",
          },
          groesseQm: "1234",
        },
        {
          angaben: {
            grundbuchblattnummer: "2",
            gemarkung: "3",
          },
          flur: {
            flur: "2",
            flurstueckZaehler: "34",
            flurstueckNenner: "56",
            wirtschaftlicheEinheitZaehler: "78.0000",
            wirtschaftlicheEinheitNenner: "90",
          },
          groesseQm: "12345",
        },
      ],
    },
    gebaeude: {
      ab1949: {
        isAb1949: "true",
      },
      baujahr: {
        baujahr: "2000",
      },
      kernsaniert: {
        isKernsaniert: "true",
      },
      kernsanierungsjahr: {
        kernsanierungsjahr: "2001",
      },
      abbruchverpflichtung: {
        hasAbbruchverpflichtung: "true",
      },
      abbruchverpflichtungsjahr: {
        abbruchverpflichtungsjahr: "2032",
      },
      wohnflaechen: ["100"],
      weitereWohnraeume: {
        hasWeitereWohnraeume: "true",
      },
      weitereWohnraeumeDetails: {
        anzahl: "2",
        flaeche: "200",
      },
      garagen: {
        hasGaragen: "true",
      },
      garagenAnzahl: {
        anzahlGaragen: "3",
      },
    },
    eigentuemer: {
      person: [
        {
          persoenlicheAngaben: {
            anrede: "frau",
            titel: "1 Titel",
            vorname: "1 Vorname",
            name: "1 Name",
            geburtsdatum: "1980-01-31",
          },
          adresse: {
            strasse: "1 Strasse",
            hausnummer: "1",
            hausnummerzusatz: "Hausnummer",
            plz: "12345",
            ort: "1 Ort",
          },
          telefonnummer: "111111",
          steuerId: "04452397687",
          anteil: {
            zaehler: "1",
            nenner: "2",
          },
        },
        {
          persoenlicheAngaben: {
            anrede: "herr",
            titel: "2 Titel",
            vorname: "2 Vorname",
            name: "2 Name",
            geburtsdatum: "1990-02-02",
          },
          adresse: {
            strasse: "2 Strasse",
            hausnummer: "2",
            hausnummerzusatz: "Hausnummer",
            plz: "12345",
            ort: "2 Ort",
          },
          telefonnummer: "222222",
          steuerId: "03352417692",
          vertreter: {
            name: {
              anrede: "herr",
              titel: "VERT Titel",
              vorname: "VERT Vorname",
              name: "VERT Name",
            },
            adresse: {
              strasse: "VERT Strasse",
              hausnummer: "3",
              hausnummerzusatz: "VERT",
              plz: "12345",
              ort: "VERT Ort",
            },
            telefonnummer: "333333",
          },
          anteil: {
            zaehler: "3",
            nenner: "4",
          },
        },
      ],
      verheiratet: "false",
      bruchteilsgemeinschaft: {
        name: "BTG Name",
        adresse: {
          strasse: "BTG Strasse",
          hausnummer: "1",
          hausnummerzusatz: "BTG",
          plz: "12345",
          ort: "BTG Ort",
        },
      },
      empfangsbevollmaechtigter: {
        name: {
          anrede: "no_anrede",
          titel: "EMP Titel",
          vorname: "EMP Vorname",
          name: "EMP Name",
        },
        adresse: {
          postfach: "654321",
          plz: "12345",
          ort: "EMP Ort",
        },
        telefonnummer: "12345",
      },
    },
  },
  clientIdentifier: "LoadTests",
};
