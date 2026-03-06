% We store symptoms as facts: fact(symptom_name).
% Python will assert/retract these facts.

:- dynamic fact/1.

% -------- Diagnosis rules --------
% diagnose(Diagnosis, Score, Advice).

diagnose('Possible head gasket issue', 100,
         'Do not drive. Check coolant+oil mixing, seek mechanic urgently.') :-
    fact(smoke_white),
    fact(temperature_high).

diagnose('Coolant leak / radiator issue', 85,
         'Stop driving if overheating. Top up coolant (if safe), inspect leaks.') :-
    fact(temperature_high),
    fact(coolant_low).

diagnose('Oil burning (worn rings/valve seals)', 80,
         'Check oil level frequently; get compression test/engine inspection.') :-
    fact(smoke_blue).

diagnose('Too much fuel / clogged air filter', 75,
         'Check air filter, MAF sensor; consider injector/mixture inspection.') :-
    fact(smoke_black).

diagnose('Weak/Dead Battery', 70,
         'Try jump-starting; check battery terminals; test battery health.') :-
    fact(engine_does_not_crank),
    fact(dashboard_lights_dim).

diagnose('Weak Battery or Faulty Starter', 65,
         'Check battery first; if battery is good, inspect starter motor/relay.') :-
    fact(clicking_sound),
    fact(engine_does_not_start).

diagnose('Spark plug / ignition issue', 60,
         'Check spark plugs, ignition coil, and wiring. Avoid repeated cranking.') :-
    fact(engine_cranks),
    fact(not_starting),
    fact(smell_fuel).

diagnose('Fuel pump / fuel supply issue', 60,
         'Check fuel level, fuel pump fuse/relay, and fuel pump sound.') :-
    fact(engine_cranks),
    fact(not_starting),
    \+ fact(smell_fuel).

% -------- Helper: best diagnosis by highest score --------
% best_diagnosis(D, Score, Advice) finds all diagnoses and picks the highest score.

best_diagnosis(D, Score, Advice) :-
    findall((S, Dx, Adv), diagnose(Dx, S, Adv), Results),
    Results \= [],
    max_member((Score, D, Advice), Results).

% -------- Fallback if nothing matches --------
best_diagnosis('No clear diagnosis - consult a mechanic', 0,
               'Symptoms don’t match rules. Get professional inspection.') :-
    \+ diagnose(_, _, _).