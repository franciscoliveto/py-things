import json


def dump():
    datastore = {"office": {"medical": [{"room-number": 100,
                                         "use": "reception",
                                         "sq-ft": 50,
                                         "price": 75
                                         },
                                        {"room-number": 101,
                                         "use": "waiting",
                                         "sq-ft": 250,
                                         "price": 75
                                         },
                                        {"room-number": 102,
                                         "use": "examination",
                                         "sq-ft": 125,
                                         "price": 150
                                         },
                                        {"room-number": 103,
                                         "use": "examination",
                                         "sq-ft": 125,
                                         "price": 150
                                         },
                                        {"room-number": 104,
                                         "use": "office",
                                         "sq-ft": 150,
                                         "price": 100
                                         }
                                        ],
                            "parking": {"location": "premium",
                                        "style": "covered",
                                        "price": 750
                                        }
                            }
                 }

    with open('datastore.json', 'w') as f:
        json.dump(datastore, f)


def load():
    with open('datastore.json', 'r') as f:
        datastore = json.load(f)

    medicals = datastore['office']['medical']
    for m in medicals:
        for k, v in m.items():
            print(k, v)
        print()


if __name__ == "__main__":
    # dump()
    load()
