% Gender Facts
male(aon).
male(wasay).
male(sajid).
male(mehdi).
male(abid).
male(nisar).
male(iftikhar).
male(abrar).
male(imran).
male(kamran).
male(javed).
male(naveed).
male(nadeem).
male(haji_maqbool).
male(saghir_sahb).
male(umar).
male(riyan).
male(sidique).
male(irshad).
male(asif).
male(nasir).
male(zafar).
male(dawood).
male(husnain).
male(zain).
male(zaid).
male(asad).
male(abdulahad).
male(saqib).

female(huda).
female(arfa).
female(saima).
female(iram).
female(kiran).
female(fiza).
female(naheed).
female(hanifa).
female(jamila).
female(fouzia).
female(unaiza).
female(shakeel_bibi).
female(makbool_bibi).
female(shehnaz).
female(mehvish).
female(waizah).
female(inshara).
female(ashi).
female(sadia).


% DOBs
dob(aon, date(2002,1,1)).
dob(ali, date(2000,1,1)).
dob(wasay, date(1993,1,1)).
dob(sajid, date(1957,1,1)).
dob(nisar, date(1948,1,1)).
dob(iftikhar, date(1940,1,1)).
dob(abrar, date(1953,1,1)).
dob(mehdi, date(1948,1,1)).
dob(abid, date(1927,1,1)).
dob(huda, date(1995,1,1)).
dob(arfa, date(1998,1,1)).
dob(fiza, date(1948,1,1)).
dob(saima, date(1966,1,1)).
dob(kiran, date(1970,1,1)).
dob(iram, date(1973,1,1)).
dob(sidique, date(1945,1,1)).
dob(irshad, date(1940,1,1)).
dob(asif, date(1973,1,1)).
dob(nasir, date(1974,1,1)).
dob(zafar, date(1970,1,1)).
dob(dawood, date(2002,1,1)).
dob(husnain, date(1998,1,1)).
dob(zain, date(2000,1,1)).
dob(zaid, date(2005,1,1)).
dob(asad, date(2007,1,1)).
dob(abdulahad, date(2012,1,1)).
dob(naheed, date(1975,1,1)).
dob(hanifa, date(1945,1,1)).
dob(jamila, date(1949,1,1)).
dob(nadeem, date(1975,1,1)).
dob(shehnaz, date(1977,1,1)).
dob(imran, date(1979,1,1)).
dob(fouzia, date(1983,1,1)).
dob(kamran, date(1985,1,1)).
dob(unaiza, date(2005,1,1)).
dob(inshara, date(2010,1,1)).
dob(mehvish, date(1991,1,1)).
dob(waizah, date(2007,1,1)).
dob(haji_maqbool, date(1935,1,1)).
dob(javed, date(1983,1,1)).
dob(saqib, date(1976,1,1)).
dob(naveed, date(1983,1,1)).
dob(saghir_sahb, date(1955,1,1)).
dob(shakeel_bibi, date(1958,1,1)).
dob(makbool_bibi, date(1965,1,1)).
dob(umar, date(2008,1,1)).
dob(riyan, date(2013,1,1)).
dob(ashi, date(1985,1,1)).
dob(sadia, date(1984,1,1)).

% Parent Facts
% Mehdi's family
parent(mehdi, sajid).
parent(mehdi, nisar).
parent(mehdi, iftikhar).
parent(mehdi, abrar).

% Abid's family
parent(abid, saima).
parent(abid, iram).
parent(abid, kiran).
parent(fiza, saima).
parent(fiza, iram).
parent(fiza, kiran).

% Sajid 's family
parent(sajid, aon).
parent(sajid, ali).
parent(sajid, wasay).
parent(sajid, huda).
parent(sajid, arfa).
parent(saima, aon).
parent(saima, ali).
parent(saima, wasay).
parent(saima, huda).
parent(saima, arfa).

% Sidique's family
parent(sidique, asif).
parent(jamila, asif).
parent(sidique, nasir).
parent(jamila, nasir).
parent(sidique, zafar).
parent(jamila, zafar).

% Irshad's family
parent(irshad, naheed).
parent(hanifa, naheed).

% Asif's family
parent(asif, dawood).
parent(naheed, dawood).
parent(asif, husnain).
parent(naheed, husnain).
parent(asif, zain).
parent(naheed, zain).
parent(asif, zaid).
parent(naheed, zaid).
parent(asif, asad).
parent(naheed, asad).
parent(asif, abdulahad).
parent(naheed, abdulahad).

% Saghir Sahb's family
parent(saghir_sahb, saqib).
parent(makbool_bibi, saqib).
parent(saghir_sahb, naveed).
parent(makbool_bibi, naveed).
parent(saghir_sahb, kamran).
parent(makbool_bibi, kamran).

% Haji Maqbool's family
parent(haji_maqbool, fouzia).
parent(shakeel_bibi, fouzia).
parent(haji_maqbool, mehvish).
parent(shakeel_bibi, mehvish).
parent(haji_maqbool, shehnaz).
parent(shakeel_bibi, shehnaz).
parent(haji_maqbool, imran).
parent(shakeel_bibi, imran).

% Imran's family
parent(imran, waizah).
parent(sadia, waizah).
parent(imran, riyan).
parent(sadia, riyan).

% Javed's family
parent(javed, inshara).
parent(ashi, inshara).

% Nadeem's family
parent(nadeem, umar).
parent(shehnaz, umar).

% Saqib's family
parent(saqib, unaiza).
parent(fouzia, unaiza).

% Marriages
married(abid, fiza).
married(sajid, saima).
married(sidique, jamila).
married(irshad, hanifa).
married(asif, naheed).
married(saghir_sahb, makbool_bibi).
married(haji_maqbool, shakeel_bibi).
married(imran, sadia).
married(javed, ashi).
married(nadeem, shehnaz).
married(saqib, fouzia).

% Western Family Relationships
father(X,Y) :- male(X), parent(X,Y).
mother(X,Y) :- female(X), parent(X,Y).
child(X,Y) :- parent(Y,X).
son(X,Y) :- male(X), parent(Y,X).
daughter(X,Y) :- female(X), parent(Y,X).

% Siblings
sibling(X,Y) :- parent(Z,X), parent(Z,Y), X \= Y.
brother(X,Y) :- male(X), sibling(X,Y).
sister(X,Y) :- female(X), sibling(X,Y).

% Grandparents
grandfather(X,Y) :- male(X), parent(X,Z), parent(Z,Y).
grandmother(X,Y) :- female(X), parent(X,Z), parent(Z,Y).
grandchild(X,Y) :- parent(Y,Z), parent(Z,X).
grandson(X,Y) :- male(X), grandchild(X,Y).
granddaughter(X,Y) :- female(X), grandchild(X,Y).

% Piblings (parent's siblings)
pibling(X,Y) :- (sibling(X,Z), parent(Z,Y)).

% Parental uncles/aunts
p_uncle(X,Y) :- male(X), parent(Z,Y), brother(X,Z).
p_aunt(X,Y) :- female(X), parent(Z,Y), sister(X,Z).

% Nephew/Niece
nephew(X,Y) :- male(X), sibling(Y,Z), parent(X,Z).
niece(X,Y) :- female(X), sibling(Y,Z), parent(X,Z).

% Cousins
cousin(X,Y) :- parent(Z,X), parent(W,Y), sibling(Z,W), X \= Y.

% Helper: Older
older(X,Y) :- dob(X, date(Y1,M1,D1)), dob(Y, date(Y2,M2,D2)),
              (Y1 < Y2 ; (Y1 = Y2, M1 < M2) ; (Y1 = Y2, M1 = Y2, D1 < D2)).



% Eastern Family Relationships

% Abu/Ami (already there)
abu(X,Y) :- father(X,Y).
ami(X,Y) :- mother(X,Y).

% Taya/Tayi (Father's elder brother/sister-in-law)
taya(X,Y) :- male(X), father(Z,Y), brother(X,Z), older(X,Z).
tayi(X,Y) :- female(X), taya(H,Y), married(H,X).

% Chacha/Chachi (Father's younger brother/sister-in-law)
chacha(X,Y) :- male(X), father(Z,Y), brother(X,Z), \+ older(X,Z).
chachi(X,Y) :- female(X), chacha(H,Y), married(H,X).

% Mama/Mami (Mother's brother/sister-in-law)
mama(X,Y) :- male(X), mother(Z,Y), brother(X,Z).
mami(X,Y) :- female(X), mama(H,Y), married(H,X).

% Khala/Khalu (Mother's sister/brother-in-law)
khala(X,Y) :- female(X), mother(Z,Y), sister(X,Z).
khalu(X,Y) :- male(X), khala(H,Y), married(H,X).

% Dada/Dadi (Father's parents)
dada(X,Y) :- male(X), parent(X,Z), father(Z,Y).
dadi(X,Y) :- female(X), parent(X,Z), father(Z,Y).

% Nana/Nani (Mother's parents)
nana(X,Y) :- male(X), parent(X,Z), mother(Z,Y).
nani(X,Y) :- female(X), parent(X,Z), mother(Z,Y).

% Dewar/Dewrani (Husband's younger brother and his wife)
dewar(X,Y) :- wife(Y,Z), brother(X,Z), \+ older(X,Z).
dewrani(X,Y) :- dewar(Z,Y), wife(X,Z).

% Jeth/Jethani (Husband's elder brother and his wife)
jeth(X,Y) :- wife(Y,Z), brother(X,Z), older(X,Z).
jethani(X,Y) :- jeth(Z,Y), wife(X,Z).

% Saas/Sasur (Husband/Wife's parents)
saas(X,Y) :- (wife(Y,Z) ; husband(Y,Z)), mother(X,Z).
sasur(X,Y) :- (wife(Y,Z) ; husband(Y,Z)), father(X,Z).

% Nand (Husband's sister)
nand(X,Y) :- wife(Y,Z), sister(X,Z).

% Bahu (Daughter-in-law)
bahu(X,Y) :- wife(X,Z), son(Z,Y).

% Damad (Son-in-law)
damad(X,Y) :- husband(X,Z), daughter(Z,Y).


% Saala/Saali (Wife's brother/sister)
saala(X,Y) :- husband(Y,Z), brother(X,Z).
saali(X,Y) :- husband(Y,Z), sister(X,Z).

% Bhanoyi (Husband of sister)
bhanoyi(X,Y) :- sister(S,Y), married(X,S).


% Beta and Beti
beta(X,Y) :- son(X,Y).         % X is beta (son) of Y
beti(X,Y) :- daughter(X,Y).    % X is beti (daughter) of Y

% Bhai and Behn
bhai(X,Y) :- male(X), sibling(X,Y).
behn(X,Y) :- female(X), sibling(X,Y).

% Bhatija and Bhatiji (Brother's children)
bhatija(X,Y) :- male(X), parent(Y,Z), brother(Y,W), parent(W,X).
bhatiji(X,Y) :- female(X), parent(Y,Z), brother(Y,W), parent(W,X).

% Pota and Poti (Son's children)
pota(X,Y) :- male(X), father(Z,Y), son(Z,X).
poti(X,Y) :- female(X), father(Z,Y), son(Z,X).

% Nawasa and Nawasi (Daughter's children)
nawasa(X,Y) :- male(X), mother(Z,Y), daughter(Z,X).
nawasi(X,Y) :- female(X), mother(Z,Y), daughter(Z,X).

% Bhanja and Bhanji (Sister's children)

bhanja(X,Y) :- male(X), behn(Y,Z), parent(X,Z).
bhanji(X,Y) :- female(X), behn(Y,Z), parent(X,Z).



