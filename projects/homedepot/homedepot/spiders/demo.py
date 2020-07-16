# -*- coding: utf-8 -*-
import json
import re
import time

import scrapy


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['homedepot.com']
    start_urls = [
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Nail-Guns-Brad-Nailers/N-5yc1vZc9nm',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Nail-Guns-Finishing-Nailers/N-5yc1vZc2be',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Nail-Guns-Framing-Nailers/N-5yc1vZc2bf',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Nail-Guns-Roofing-Nailers/N-5yc1vZc28n',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Nail-Guns-Flooring-Nailers/N-5yc1vZc2ak',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Nail-Guns-Metal-Connector-Nailers/N-5yc1vZc2ce',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Nail-Guns-Palm-Nailers/N-5yc1vZc9ng',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Nail-Guns-Pin-Nailers/N-5yc1vZc9n5',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Nail-Guns-Specialty-Nailers/N-5yc1vZc297',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Pneumatic-Staplers/N-5yc1vZc2eu',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Air-Compressors-Portable-Air-Compressors/N-5yc1vZc9pn',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Air-Compressors-Stationary-Air-Compressors/N-5yc1vZc9pi',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Air-Compressors/N-5yc1vZc27pZ1z0ryv5',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Air-Compressors/Electric/N-5yc1vZc27pZ1z0r88l',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Air-Compressors/Gas/N-5yc1vZc27pZ1z0r88j',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Air-Compressors/Rechargeable-Battery/N-5yc1vZc27pZ1z0ls49',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Inflators/Corded/N-5yc1vZc285Z1z1a98n',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Inflators/Cordless/N-5yc1vZc285Z1z1a9cv',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Air-Tools-Air-Impact-Wrenches/N-5yc1vZc9no',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Air-Tools-Air-Grease-Guns/N-5yc1vZc9na',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Air-Tools-Air-Blow-Guns/N-5yc1vZc9nv',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Air-Compressor-Parts-Accessories-Air-Hoses/N-5yc1vZc9nn',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Air-Compressor-Parts-Accessories-Air-Tool-Fittings/N-5yc1vZc9nb',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Air-Compressor-Parts-Accessories-Air-Pressure-Regulators/N-5yc1vZc9n7',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories/RYOBI/N-5yc1vZc2fhZm5d',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories/RIDGID/Ridgid/N-5yc1vZc2fhZ18gZ1a3',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories/DEWALT/N-5yc1vZc2fhZ4j2',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories/Husky/N-5yc1vZc2fhZrd',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories/Porter-Cable/N-5yc1vZc2fhZ68y',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories/California-Air-Tools/N-5yc1vZc2fhZ8te',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories/Milwaukee/N-5yc1vZc2fhZzv',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories/EMAX/N-5yc1vZc2fhZ50u',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories/Ingersoll-Rand/N-5yc1vZc2fhZ8rc',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories/Makita/N-5yc1vZc2fhZyg',
        'https://www.homedepot.com/b/Automotive-Cargo-Carriers-Bike-Racks/N-5yc1vZclaa',
        'https://www.homedepot.com/b/Automotive-Cargo-Carriers-Cargo-Boxes-Bags/N-5yc1vZ2fkok8i',
        'https://www.homedepot.com/b/Automotive-Cargo-Carriers-Hitch-Cargo-Carriers/N-5yc1vZ2fkok86',
        'https://www.homedepot.com/b/Automotive-Cargo-Carriers-Roof-Racks/N-5yc1vZ2fkok8c',
        'https://www.homedepot.com/b/Automotive-Towing-Equipment-Tow-Ropes-Cables-Chains/N-5yc1vZc8m8',
        'https://www.homedepot.com/b/Automotive-Towing-Equipment-Utility-Trailers/N-5yc1vZc8m7',
        'https://www.homedepot.com/b/Automotive-Car-Fluids-Chemicals/N-5yc1vZcla3',
        'https://www.homedepot.com/b/Automotive-Shop-Equipment-Car-Lifts/N-5yc1vZc8mw',
        'https://www.homedepot.com/b/Automotive-Shop-Equipment-Car-Jacks/N-5yc1vZc8mp',
        'https://www.homedepot.com/b/Automotive-Shop-Equipment-Car-Jacks-Jack-Stands/N-5yc1vZ2fkoo14',
        'https://www.homedepot.com/b/Automotive-Shop-Equipment-Engine-Stands/N-5yc1vZ2fkoo1a',
        'https://www.homedepot.com/b/Automotive-Shop-Equipment-Engine-Hoists/N-5yc1vZclaz',
        'https://www.homedepot.com/b/Automotive-Shop-Equipment-Car-Ramps/N-5yc1vZ2fkowl3',
        'https://www.homedepot.com/b/Automotive-Battery-Charging-Systems-Car-Batteries/N-5yc1vZc8mx',
        'https://www.homedepot.com/b/Automotive-Battery-Charging-Systems-Jumper-Cables/N-5yc1vZc8mb',
        'https://www.homedepot.com/b/Automotive-Battery-Charging-Systems-Car-Battery-Chargers/N-5yc1vZc8mm',
        'https://www.homedepot.com/b/Automotive-Battery-Charging-Systems-Car-Power-Inverters/N-5yc1vZc8na',
        'https://www.homedepot.com/b/Automotive-Tire-Accessories/N-5yc1vZc8sw',
        'https://www.homedepot.com/b/Automotive-Interior-Car-Accessories-Cargo-Mats/N-5yc1vZc8n3',
        'https://www.homedepot.com/b/Automotive-Exterior-Car-Accessories-Car-Covers/N-5yc1vZc8md',
        'https://www.homedepot.com/b/Automotive-Exterior-Car-Accessories-Off-Road-Lights/N-5yc1vZclrj',
        'https://www.homedepot.com/b/Automotive-Exterior-Car-Accessories-Winches/N-5yc1vZc8st',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Bull-Bars-Grille-Guards/N-5yc1vZ2fkokee',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Bumpers/N-5yc1vZ2fkokdw',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Cowl-Panels/N-5yc1vZ2fkoki2',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Fender-Flares-and-Liners/N-5yc1vZ2fkokg9',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Tailgates/N-5yc1vZ2fkokbs',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Truck-Bed-Accessories/N-5yc1vZclau',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Truck-Bed-Liners/N-5yc1vZ2fkokba',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Window-Deflectors/N-5yc1vZ2fkok9x',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Truck-Tool-Boxes-Chest-Truck-Tool-Boxes/N-5yc1vZ2fkok7z',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Truck-Tool-Boxes-Crossover-Truck-Tool-Boxes/N-5yc1vZ2fkok80',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Truck-Tool-Boxes-Side-Truck-Tool-Boxes/N-5yc1vZ2fkok8e',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Truck-Tool-Boxes-Trailer-Tongue-Boxes/N-5yc1vZ2fkok8l',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Truck-Tool-Boxes-Transfer-Tanks/N-5yc1vZ2fkok8n',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Truck-Tool-Boxes-Truck-Bed-Storage-Drawers/N-5yc1vZ2fkok7y',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Truck-Tool-Boxes-Truck-Tool-Box-Accessories/N-5yc1vZ2fkok8s',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Truck-Tool-Boxes-Underbody-Tool-Boxes/N-5yc1vZ2fkok8j',
        'https://www.homedepot.com/b/Automotive-Truck-Accessories-Truck-Tool-Boxes-Wheel-Well-Tool-Boxes/N-5yc1vZ2fkok7v',
        'https://www.homedepot.com/b/Paint-Industrial-Commercial-Paint-Automotive-Paint/N-5yc1vZc616',
        'https://www.homedepot.com/b/Tools-Hand-Tools-Hand-Tool-Sets-Mechanics-Tool-Sets/N-5yc1vZc90m',
        'https://www.homedepot.com/b/Automotive/Weather-Guard/N-5yc1vZc8o1Zdpf',
        'https://www.homedepot.com/b/Automotive/Dannmar/N-5yc1vZc8o1Zc73',
        'https://www.homedepot.com/b/Automotive/DEWALT/N-5yc1vZc8o1Z4j2',
        'https://www.homedepot.com/b/Tools-Hand-Tools-Chisels-Files-Punches/N-5yc1vZc97x',
        'https://www.homedepot.com/b/Tools-Hand-Tools-Cutting-Tools/N-5yc1vZc21j',
        'https://www.homedepot.com/b/Tools-Hand-Tools-Hammers/N-5yc1vZc98g',
        'https://www.homedepot.com/b/Tools-Hand-Tools-Hex-Keys/N-5yc1vZc265',
        'https://www.homedepot.com/b/Automotive-Car-Fluids-Chemicals/N-5yc1vZ2fkot4v',
        'https://www.homedepot.com/b/Tools-Hand-Tools-Stud-Finders/N-5yc1vZc23h',
        'https://www.homedepot.com/b/Tools-Hand-Tools-Tool-Accessories/N-5yc1vZc1zw',
        'https://www.homedepot.com/b/Tools-Hand-Tools-Wrecking-Pry-Bars/N-5yc1vZc24o',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Power-Tool-Batteries/RYOBI/N-5yc1vZc809Zm5d',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Power-Tool-Batteries/Milwaukee/N-5yc1vZc809Zzv',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Power-Tool-Batteries/DEWALT/N-5yc1vZc809Z4j2',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Power-Tool-Batteries/Makita/N-5yc1vZc809Zyg',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Drill-Attachments/N-5yc1vZc26c',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Jobsite-Radios/N-5yc1vZc25a',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Oscillating-Tool-Attachments/N-5yc1vZc8y4',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Power-Tool-Batteries/N-5yc1vZc809',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Power-Tool-Battery-Chargers/N-5yc1vZc808',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Rotary-Tool-Accessories/N-5yc1vZc25m',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Saw-Accessories/N-5yc1vZ1z18gwi',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Saw-Tracks/N-5yc1vZ1z18gvi',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Sharpening-Tools/N-5yc1vZc2jd',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Specialty-Power-Tool-Accessories/N-5yc1vZc2jt',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Tool-Stands/N-5yc1vZc2jn',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories/RYOBI/N-5yc1vZc246Zm5d',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories/DIABLO/N-5yc1vZc246Zqy9',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories/Bosch/N-5yc1vZc246Z9u',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories/RIDGID/N-5yc1vZc246Z18g',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories/Makita/N-5yc1vZc246Zyg',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories/DEWALT/N-5yc1vZc246Z4j2',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories/Dremel/N-5yc1vZc246Zgr',
        'https://www.homedepot.com/b/Tools-Power-Tools-Power-Tool-Combo-Kits/Cordless/N-5yc1vZc2ecZ1z140i3',
        'https://www.homedepot.com/b/Tools-Power-Tools-Drills/Cordless/N-5yc1vZc27fZ1z140i3',
        'https://www.homedepot.com/b/Tools-Power-Tools-Saws/Cordless/N-5yc1vZc28lZ1z140i3',
        'https://www.homedepot.com/b/Tools-Power-Tools-Sanders/Cordless/N-5yc1vZc28sZ1z140i3',
        'https://www.homedepot.com/b/Tools-Power-Tools-Grinders/Cordless/N-5yc1vZc2fvZ1z140i3',
        'https://www.homedepot.com/b/Tools-Power-Tools/Cordless/0/N-5yc1vZc298Zc298Z1z0jykrZ1z140i3',
        'https://www.homedepot.com/b/RIDGID/N-5yc1vZ18g',
        'https://www.homedepot.com/b/Tools-Power-Tools/Bosch/N-5yc1vZc298Z9u',
        'https://www.homedepot.com/b/Tools-Power-Tools/Dremel/N-5yc1vZc298Zgr',
        'https://www.homedepot.com/b/Tools-Power-Tools-Drills-Power-Drills/N-5yc1vZc7jj',
        'https://www.homedepot.com/b/Tools-Power-Tools-Drills-Hammer-Drills/N-5yc1vZc8wt',
        'https://www.homedepot.com/b/Tools-Power-Tools-Drills-Right-Angle-Drills/N-5yc1vZc7ji',
        'https://www.homedepot.com/b/Tools-Power-Tools-Drills-Impact-Drivers/N-5yc1vZc29x',
        'https://www.homedepot.com/b/Tools-Power-Tools-Drills-Electric-Screwdrivers/N-5yc1vZcjnx',
        'https://www.homedepot.com/b/Tools-Power-Tools-Saws-Circular-Saws/N-5yc1vZc2dc',
        'https://www.homedepot.com/b/Tools-Power-Tools-Saws-Miter-Saws/N-5yc1vZc2d7',
        'https://www.homedepot.com/b/Tools-Power-Tools-Saws-Reciprocating-Saws/N-5yc1vZc2h7',
        'https://www.homedepot.com/b/Tools-Power-Tools-Saws-Jigsaws/N-5yc1vZc292',
        'https://www.homedepot.com/b/Tools-Power-Tools-Saws-Table-Saws/N-5yc1vZ2fkokih',
        'https://www.homedepot.com/b/Tools-Power-Tools-Saws-Concrete-Saws/N-5yc1vZc29s',
        'https://www.homedepot.com/b/Tools-Power-Tools-Woodworking-Tools-Lathes/N-5yc1vZc289',
        'https://www.homedepot.com/b/Tools-Power-Tools-Woodworking-Tools-Drill-Presses/N-5yc1vZc2dj',
        'https://www.homedepot.com/b/Tools-Power-Tools-Saws-Band-Saws-Portable-Band-Saws/N-5yc1vZc2h4',
        'https://www.homedepot.com/b/Tools-Power-Tools-Sanders/N-5yc1vZc28s',
        'https://www.homedepot.com/b/Tools-Power-Tools-Woodworking-Tools-Routers/N-5yc1vZc2h2',
        'https://www.homedepot.com/b/Tools-Power-Tools-Sanders-Belt-Sanders/N-5yc1vZc286',
        'https://www.homedepot.com/b/Tools-Power-Tools-Sanders-Disc-Orbital-Sanders/N-5yc1vZc2gb',
        'https://www.homedepot.com/b/Tools-Power-Tools-Sanders-Sheet-Sanders/N-5yc1vZc29d',
        'https://www.homedepot.com/b/Tools-Power-Tools-Sanders-Spindle-Sanders/N-5yc1vZc2gh',
        'https://www.homedepot.com/b/Tools-Air-Compressors-Tools-Accessories-Nail-Guns/N-5yc1vZc2cd',
        'https://www.homedepot.com/b/Tools-Power-Tools-Drills/Cordless/0/N-5yc1vZc27fZ1z0jykrZ1z140i3',
        'https://www.homedepot.com/b/Tools-Power-Tools-Drills-Impact-Drivers/Cordless/0/N-5yc1vZc29xZ1z0jykrZ1z140i3',
        'https://www.homedepot.com/b/Tools-Power-Tools-Concrete-Drilling-Tools/Cordless/0/N-5yc1vZc2erZ1z0jykrZ1z140i3',
        'https://www.homedepot.com/b/Tools-Power-Tools-Power-Multi-Tools-Oscillating-Tools/N-5yc1vZc2b2',
        'https://www.homedepot.com/b/Tools-Power-Tools-Power-Multi-Tools-Rotary-Tools/N-5yc1vZc2fp',
        'https://www.homedepot.com/b/Tools-Power-Tools-Concrete-Drilling-Tools-Coring-Tools/N-5yc1vZc7mt',
        'https://www.homedepot.com/b/Tools-Power-Tools-Concrete-Drilling-Tools/N-5yc1vZc2er',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Power-Tool-Batteries-Chargers/N-5yc1vZc25y',
        'https://www.homedepot.com/b/Tools-Power-Tools/Milwaukee-M18/N-5yc1vZc298Z1z17rdr',
        'https://www.homedepot.com/b/Tools-Power-Tools/Milwaukee-M12/N-5yc1vZc298Z1z17rcu',
        'https://www.homedepot.com/b/Tools-Power-Tools/Milwaukee-MX-Fuel/N-5yc1vZc298Z1z1cgih',
        'https://www.homedepot.com/b/Tools-Power-Tools/Dewalt-20v-MAX/N-5yc1vZc298Z1z17r6w',
        'https://www.homedepot.com/b/Tools-Power-Tools/Dewalt-60v-MAX-Flexvolt/N-5yc1vZc298Z1z17qm7',
        'https://www.homedepot.com/b/Tools-Power-Tools/Ryobi-18v-ONE-/N-5yc1vZc298Z1z17r9o',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/RYOBI/40/N-5yc1vZbx5cZm5dZ1z0u9q5',
        'https://www.homedepot.com/b/Tools-Power-Tools/RIDGID-12v/N-5yc1vZc298Z1z17uax',
        'https://www.homedepot.com/b/Tools-Power-Tools/RIDGID-18v/N-5yc1vZc298Z1z17uc6',
        'https://www.homedepot.com/b/Tools-Power-Tools/RIDGID-JOBMAX/N-5yc1vZc298Z1z17ugn',
        'https://www.homedepot.com/b/Tools-Power-Tools/Makita-18v-LXT/N-5yc1vZc298Z1z17rb0',
        'https://www.homedepot.com/b/Tools-Power-Tools/Makita-12v-Max/N-5yc1vZc298Z1z17qrn',
        'https://www.homedepot.com/b/Tools-Tool-Storage-Tool-Chests/N-5yc1vZc2gk',
        'https://www.homedepot.com/b/Tools-Tool-Storage-Tool-Chests-Mobile-Workbenches/N-5yc1vZcerm',
        'https://www.homedepot.com/b/Tools-Tool-Storage-Portable-Tool-Boxes/N-5yc1vZc22a',
        'https://www.homedepot.com/b/Tools-Tool-Storage-Tool-Bags/N-5yc1vZc2g6',
        'https://www.homedepot.com/b/Tools-Tool-Storage-Tool-Belts/N-5yc1vZc27z',
        'https://www.homedepot.com/b/Tools-Tool-Storage-Jobsite-Boxes/N-5yc1vZc27g',
        'https://www.homedepot.com/b/Tools-Tool-Storage/Interlocking-Storage-System/N-5yc1vZc22eZ1z196e6',
        'https://www.homedepot.com/b/Tools-Tool-Storage-Tool-Storage-Accessories/N-5yc1vZcerq',
        'https://www.homedepot.com/b/Tools-Tool-Storage-Small-Parts-Organizers/N-5yc1vZc28p',
        'https://www.homedepot.com/b/Tools-Tool-Storage-Shelf-Bins-Racks/N-5yc1vZc22d',
        'https://www.homedepot.com/b/Tools-Tool-Storage-Tool-Storage-Accessories/Tops-Liners/N-5yc1vZcerqZ1z0l5ul',
        'https://www.homedepot.com/b/Storage-Organization-Garage-Storage-Workbenches/N-5yc1vZc898',
        'https://www.homedepot.com/b/Tools-Tool-Storage-Saw-Horses/N-5yc1vZc708',
        'https://www.homedepot.com/b/Storage-Organization-Shelving/Shelving-Units/N-5yc1vZc89kZ1z0tuqr',
        'https://www.homedepot.com/b/Safety-Equipment-Knee-Pads/N-5yc1vZc220',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Machines/N-5yc1vZc8lk',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Machines-Engine-Driven-Welders/N-5yc1vZ2fkoml9',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Machines-Wire-Feeders/N-5yc1vZ1z18gw6',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Machines-Plasma-Cutters/N-5yc1vZ1z18gva',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Machines-TIG-Welders/N-5yc1vZ1z18gw1',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Machines-MIG-Welders/N-5yc1vZ1z18gv1',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Machines-Multi-Process-Welders/N-5yc1vZ1z18gvv',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Supplies-Welding-Rods/N-5yc1vZ1z18gwg',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Supplies-Welding-Parts/N-5yc1vZ1z18gvw',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Supplies-Welding-Accessories/N-5yc1vZ1z18gvq',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Supplies-Welding-Spool-Guns/N-5yc1vZ1z18gv2',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Supplies-Welding-Wire/N-5yc1vZ1z18guy',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Supplies-Welding-Tips/N-5yc1vZ1z18gvk',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Supplies-Welding-Carts/N-5yc1vZ1z18gvc',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Supplies-Welding-Hammers/N-5yc1vZ1z18gvr',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Supplies-Welding-Brushes/N-5yc1vZ1z18gwf',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Safety-Apparel-Welding-Helmets/N-5yc1vZ1z18gwd',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Safety-Apparel-Welding-Gloves/N-5yc1vZ1z18gwm',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Welding-Safety-Apparel-Flame-Resistant-Work-Wear/N-5yc1vZ1z18gyv',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Brazing-Soldering-Equipment-Soldering-Guns/N-5yc1vZ1z18gv0',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Brazing-Soldering-Equipment-Soldering-Irons/N-5yc1vZc8lu',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Brazing-Soldering-Equipment-Soldering-Stations/N-5yc1vZ1z18gw2',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Brazing-Soldering-Equipment-Soldering-Parts-Accessories/N-5yc1vZc8lg',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Brazing-Soldering-Equipment-Solder-Solder-Flux/N-5yc1vZ1z18gvz',
        'https://www.homedepot.com/b/Tools-Welding-Soldering-Brazing-Soldering-Equipment-Solder-Solder-Wire/N-5yc1vZ1z18gvg',
        'https://www.homedepot.com/b/Tools-Welding-Soldering/Lincoln-Electric/N-5yc1vZc8lpZwp',
        'https://www.homedepot.com/b/Tools-Welding-Soldering/Bernzomatic/N-5yc1vZc8lpZ91',
        'https://www.homedepot.com/b/Tools-Welding-Soldering/Forney/N-5yc1vZc8lpZeks',
        'https://www.homedepot.com/b/Tools-Welding-Soldering/Weller/N-5yc1vZc8lpZ1lw',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Base-Layers/N-5yc1vZcl3n',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Bib-Overalls/N-5yc1vZc4oi',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Coveralls/N-5yc1vZc4og',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Outerwear-Work-Hoodies-Sweatshirts/N-5yc1vZcl41',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Outerwear-Work-Jackets/N-5yc1vZc3vl',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Work-Hats/N-5yc1vZcl3v',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Work-Pants/N-5yc1vZc4oh',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Work-Shirts/N-5yc1vZc4oo',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Work-Shorts/N-5yc1vZc4ok',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Outerwear-Work-Vests/N-5yc1vZcl5k',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear/Hi-Vis/N-5yc1vZc4otZ1z18mjj',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear/Flame-Resistant/N-5yc1vZc4otZ1z17z7f',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Rain-Gear/N-5yc1vZc4ol',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Heated-Gear/N-5yc1vZcerw',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Cooling-Gear/N-5yc1vZcl4w',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Waders/N-5yc1vZcl4h',
        'https://www.homedepot.com/b/Clothing-Footwear-Hunting-Clothes-Apparel/N-5yc1vZc451',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Food-Service-Uniforms/N-5yc1vZcl5f',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Medical-Clothing/N-5yc1vZcl3l',
        'https://www.homedepot.com/b/Paint-Paint-Tools-Supplies-Paint-Apparel-Safety-Accessories-Painters-Clothing/N-5yc1vZcic3',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Work-Aprons/N-5yc1vZcl3k',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Work-Belts/N-5yc1vZcl43',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Work-Suspenders/N-5yc1vZcl3e',
        'https://www.homedepot.com/b/Clothing-Footwear-Footwear-Work-Shoes/N-5yc1vZcl58',
        'https://www.homedepot.com/b/Clothing-Footwear-Footwear-Rubber-Boots/N-5yc1vZcl57',
        'https://www.homedepot.com/b/Clothing-Footwear-Footwear-Hunting-Boots/N-5yc1vZc416',
        'https://www.homedepot.com/b/Clothing-Footwear-Footwear-Tactical-Boots/N-5yc1vZcl5p',
        'https://www.homedepot.com/b/Safety-Equipment-Disposable-Protective-Clothing-Disposable-Shoe-Covers/N-5yc1vZclln',
        'https://www.homedepot.com/b/Clothing-Footwear-Workwear-Work-Socks/N-5yc1vZcl3c',
        'https://www.homedepot.com/b/Clothing-Footwear-Footwear-Insoles/N-5yc1vZc70l',
        'https://www.homedepot.com/b/Clothing-Footwear-Footwear-Overshoes/N-5yc1vZcl2t',
        'https://www.homedepot.com/b/Safety-Equipment-Protective-Eyewear/N-5yc1vZclho',
        'https://www.homedepot.com/b/Safety-Equipment-Hearing-Protection/N-5yc1vZc22t',
        'https://www.homedepot.com/b/Safety-Equipment-Respirator-Masks/N-5yc1vZc25k',
        'https://www.homedepot.com/b/Safety-Equipment-Head-Protection/N-5yc1vZclgo',
        'https://www.homedepot.com/b/Safety-Equipment-Fall-Protection-Equipment/N-5yc1vZbzzj',
        'https://www.homedepot.com/b/Safety-Equipment-Disposable-Protective-Clothing/N-5yc1vZcljk',
        'https://www.homedepot.com/b/Safety-Equipment-Protective-Eyewear-Safety-Glasses-Sunglasses/N-5yc1vZc1xt',
        'https://www.homedepot.com/b/Safety-Equipment-Protective-Eyewear-Safety-Goggles/N-5yc1vZcll9',
        'https://www.homedepot.com/b/Safety-Equipment-Head-Protection-Hard-Hats/N-5yc1vZc22l',
        'https://www.homedepot.com/b/Safety-Equipment-Head-Protection-Bump-Caps/N-5yc1vZcljm',
        'https://www.homedepot.com/b/Safety-Equipment-Head-Protection-Face-Shields/N-5yc1vZclhu',
        'https://www.homedepot.com/b/Safety-Equipment-Hearing-Protection-Ear-Muffs/N-5yc1vZclh9',
        'https://www.homedepot.com/b/Safety-Equipment-Hearing-Protection-Ear-Plugs/N-5yc1vZclkb',
        'https://www.homedepot.com/b/Safety-Equipment-Safety-Vests/N-5yc1vZc29h',
        'https://www.homedepot.com/b/Safety-Equipment-Back-Support-Belts/N-5yc1vZc23q',
        'https://www.homedepot.com/b/Safety-Equipment-Fall-Protection-Equipment-Safety-Harnesses/N-5yc1vZbzzi',
        'https://www.homedepot.com/b/Safety-Equipment-Fall-Protection-Equipment-Anchor-Points/N-5yc1vZbzzq',
        'https://www.homedepot.com/b/Safety-Equipment-Fall-Protection-Equipment-Lanyards/N-5yc1vZclhc',
        'https://www.homedepot.com/b/Safety-Equipment-Fall-Protection-Equipment-Self-Retracting-Lifelines/N-5yc1vZbzzh',
        'https://www.homedepot.com/b/Safety-Equipment-Fall-Protection-Equipment-Lifelines/N-5yc1vZclh7',
        'https://www.homedepot.com/b/Safety-Equipment-PPE-Kits/N-5yc1vZcllt',
        'https://www.homedepot.com/b/Safety-Equipment-Disposable-Protective-Clothing-Disposable-Gloves/N-5yc1vZclhn',
        'https://www.homedepot.com/b/Safety-Equipment-Disposable-Protective-Clothing-Disposable-Coveralls/N-5yc1vZclhs',
        'https://www.homedepot.com/b/Tools-Safety-Security-Home-Safety-Emergency-Preparedness-First-Aid-Kits/N-5yc1vZc26u',
        'https://www.homedepot.com/b/Tools-Safety-Security-Home-Safety-Emergency-Preparedness-Emergency-Response-Kits/N-5yc1vZc26t',
        'https://www.homedepot.com/b/Safety-Equipment-Eyewash-Stations-Emergency-Showers/N-5yc1vZclix',
        'https://www.homedepot.com/b/Safety-Equipment-Testing-Instruments/N-5yc1vZc28g',
        'https://www.homedepot.com/b/Safety-Equipment/3M/N-5yc1vZc4owZ30',
        'https://www.homedepot.com/b/Safety-Equipment/DEWALT/N-5yc1vZc4owZ4j2',
        'https://www.homedepot.com/b/Safety-Equipment/Milwaukee/N-5yc1vZc4owZzv',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/RYOBI/N-5yc1vZbx5cZm5d',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/Toro/N-5yc1vZbx5cZ1i9',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/Honda/N-5yc1vZbx5cZ3le',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/EGO/N-5yc1vZbx5cZd9q',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/Cub-Cadet/N-5yc1vZbx5cZeb',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/ECHO/N-5yc1vZbx5cZ36i',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/Troy-Bilt/N-5yc1vZbx5cZmp3',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/John-Deere/N-5yc1vZbx5cZt7',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/BLACK-DECKER/N-5yc1vZbx5cZe7c',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/Briggs-Stratton/N-5yc1vZbx5cZa8',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/Generac/N-5yc1vZbx5cZ4ph',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/Sun-Joe/N-5yc1vZbx5cZ6e3',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/Champion-Power-Equipment/N-5yc1vZbx5cZ9xs',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/Westinghouse/N-5yc1vZbx5cZ1m6',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/Skil/N-5yc1vZbx5cZ1dk',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Lawn-Mowers/N-5yc1vZc5ar',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Lawn-Mowers-Self-Propelled-Lawn-Mowers/N-5yc1vZc5ap',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Riding-Lawn-Mowers-Zero-Turn-Mowers/N-5yc1vZc5ak',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Trimmers-String-Trimmers/N-5yc1vZbx8i',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Trimmers-Hedge-Trimmers/N-5yc1vZbx9r',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Trimmers-Edgers/N-5yc1vZbxdg',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Leaf-Blowers/Backpack-Blower/N-5yc1vZbxavZ1z0tgy3',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Leaf-Blowers/Handheld-Blower/Handheld-Blower-Vacuum/N-5yc1vZbxavZ1z0tgy2Z1z0tgyc',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Chainsaws-Pole-Saws/N-5yc1vZbxaj',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Chipper-Shredders/N-5yc1vZbxbi',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Log-Splitters/N-5yc1vZbxag',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Stump-Grinders/N-5yc1vZc4dy',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Snow-Removal-Equipment-Snow-Blowers-Gas-Snow-Blowers/N-5yc1vZceo5',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Snow-Removal-Equipment-Snow-Blowers-Cordless-Snow-Blowers/N-5yc1vZcem5',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Snow-Removal-Equipment-Snow-Blowers-Electric-Snow-Blowers/N-5yc1vZcema',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Augers/N-5yc1vZbxda',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Rototillers-Cultivators/N-5yc1vZbxce',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Plate-Compactors/N-5yc1vZc4du',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Replacement-Engines-Parts-Replacement-Parts-Outdoor-Power-Batteries-Chargers/N-5yc1vZbxd3',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Replacement-Engines-Parts-Replacement-Parts-Belts/N-5yc1vZbx9v',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Replacement-Engines-Parts-Maintenance-Parts-Lawn-Mower-Blades/N-5yc1vZbxci',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Replacement-Engines-Parts-Replacement-Parts-Replacement-Engines/N-5yc1vZbxdk',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Replacement-Engines-Parts-Maintenance-Parts-Lawn-Mower-Filters/N-5yc1vZbx8x',
        'https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Replacement-Engines-Parts-Replacement-Parts-Replacement-Wheels/N-5yc1vZbx90',
        'https://www.homedepot.com/b/Heating-Venting-Cooling-Fans-Blower-Fans/Commercial/Commercial-Residential/N-5yc1vZc4m7Z1z0y7p7Z1z11e9p',
        'https://www.homedepot.com/b/Heating-Venting-Cooling-Fans-Blower-Fans/Bulk-Set/N-5yc1vZc4m7Z1z17nn0',
        'https://www.homedepot.com/b/Heating-Venting-Cooling-Fans-Blower-Fans/Contractor-Pack/N-5yc1vZc4m7Z1z1bazb',
        'https://www.homedepot.com/b/Heating-Venting-Cooling-Fans-Blower-Fans/Commercial-Residential/Residential/N-5yc1vZc4m7Z1z0y7p7Z1z12x7x',
        'https://www.homedepot.com/b/Heating-Venting-Cooling-Air-Quality-Dehumidifiers/Commercial/N-5yc1vZc4l8Z1z11e9p',
        'https://www.homedepot.com/b/Heating-Venting-Cooling-Air-Quality-Dehumidifiers/Bulk-Set/N-5yc1vZc4l8Z1z17nn0',
        'https://www.homedepot.com/b/Heating-Venting-Cooling-Air-Quality-Dehumidifiers/Residential/N-5yc1vZc4l8Z1z12x7x',
        'https://www.homedepot.com/b/Heating-Venting-Cooling-Air-Quality-Air-Purifiers/Commercial/N-5yc1vZc4m5Z1z0mxuh',
        'https://www.homedepot.com/b/Heating-Venting-Cooling-Air-Quality-Air-Purifiers/Personal/N-5yc1vZc4m5Z1z0vuav',
        'https://www.homedepot.com/b/Tools-Shop-Vacuums/N-5yc1vZc2a7',
        'https://www.homedepot.com/b/Tools-Power-Tools-Drills-Rotary-Hammers/N-5yc1vZc8wv',
        'https://www.homedepot.com/b/Tools-Power-Tools-Concrete-Drilling-Tools-Demolition-Breaker-Hammers/Wall/N-5yc1vZc2cnZ1z18by4',
        'https://www.homedepot.com/b/Tools-Power-Tools-Concrete-Drilling-Tools-Demolition-Breaker-Hammers/Floor/N-5yc1vZc2cnZ1z18bxh',
        'https://www.homedepot.com/b/Tools-Power-Tools-Grinders-Angle-Grinders/12-in/14-in/7/7-in/9/9-in/N-5yc1vZc2fwZ1z0t8v1Z1z0twhtZ1z0uj6wZ1z0uj7vZ1z0uj8mZ1z0uj99',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Drill-Bits-Masonry-Drill-Bits/Flat-Chisel/Point-Chisel/Spade-Chisel/Concrete/N-5yc1vZc23fZ1z0lfecZ1z0lxpbZ1z0m6ihZ1z0mzpu',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Saw-Blades-Diamond-Blades/N-5yc1vZc5v1',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Abrasives-Grinder-Accessories-Grinding-Wheels-Cut-Off-Wheels/N-5yc1vZc8y5',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Drill-Bits-Masonry-Drill-Bits/Masonry-Bit/N-5yc1vZc23fZ1z0sjdx',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Drill-Bits/Concrete/N-5yc1vZc248Z1z0mzpu',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Drill-Bits-Coring-Drill-Bits/N-5yc1vZc7mq',
        'https://www.homedepot.com/b/Tools-Power-Tools-Woodworking-Tools-Dust-Collectors-Air-Filtration/Air-Filtration-System/Dust-Extractor-Vacuum/N-5yc1vZc2d1Z1z0qwp6Z1z0qwp8',
        'https://www.homedepot.com/b/Tools-Power-Tools-Woodworking-Tools-Dust-Collectors-Air-Filtration/Dust-Collector/N-5yc1vZc2d1Z1z0qwq3',
        'https://www.homedepot.com/b/Tools-Power-Tools-Woodworking-Tools-Dust-Collectors-Air-Filtration/Accessory/Accessory-Kit/Attachment/Filter/Filter-Bag/Hose/N-5yc1vZc2d1Z1z0qwnbZ1z0qwp7Z1z0qwpaZ1z0qwqaZ1z0qwqcZ1z0qwqg',
        'https://www.homedepot.com/b/Tools-Power-Tools-Power-Crimpers/N-5yc1vZ1z18g92',
        'https://www.homedepot.com/b/Electrical-Electrical-Tools-Electrical-Testers/N-5yc1vZboff',
        'https://www.homedepot.com/b/Plumbing-Drain-Openers-Drain-Snakes/110-Volt/Electric/Electrical-Outlet/Other/N-5yc1vZbqoeZ1z106n7Z1z107ciZ1z107vvZ1z1083v',
        'https://www.homedepot.com/b/Plumbing-Plumbing-Tools-Pipe-Tube-Cutters/N-5yc1vZc4ft',
        'https://www.homedepot.com/b/Plumbing-Plumbing-Tools-Pipe-Fitting-Tools-Expansion-Tools/N-5yc1vZcl1u',
        'https://www.homedepot.com/b/Plumbing-Plumbing-Tools-Pipe-Tube-Benders/N-5yc1vZc4g6',
        'https://www.homedepot.com/b/Tools-Power-Tools-Saws-Chop-Saws/N-5yc1vZc2f6',
        'https://www.homedepot.com/b/Tools-Power-Tool-Accessories-Saw-Blades/Metal/N-5yc1vZc2jyZ1z13133',
        'https://www.homedepot.com/b/Tools/Bosch/N-5yc1vZc1xyZ9u?Ns=P_REP_PRC_MODE%7C1',
        'https://www.homedepot.com/b/Tools/Hilti/N-5yc1vZc1xyZpx',
        'https://www.homedepot.com/b/Tools/RIDGID/N-5yc1vZc1xyZ18g?Ns=P_REP_PRC_MODE%7C1',
        'https://www.homedepot.com/b/Lighting-Commercial-Lighting-Work-Lights/N-5yc1vZcgdu',
        'https://www.homedepot.com/b/Tools-Power-Tools-Jobsite-Jobsite-Audio/N-5yc1vZclr6',
        'https://www.homedepot.com/b/Tools-Power-Tools-Jobsite-Tool-Tracking/N-5yc1vZclr8',
        'https://www.homedepot.com/b/Tools-Power-Tools-Jobsite-Jobsite-Fans/N-5yc1vZclr7',
        'https://www.homedepot.com/b/Tools-Safety-Security-Cable-Locks/N-5yc1vZ2fkoq90',
        'https://www.homedepot.com/b/Tools-Safety-Security-Padlocks/N-5yc1vZc23a',
        'https://www.homedepot.com/b/Tools-Safety-Security-Safes/N-5yc1vZc2b1',
        'https://www.homedepot.com/b/Hardware-Tie-Down-Straps/N-5yc1vZc2dn']

    custom_settings = {
        'LOG_LEVEL': 'INFO',
        # 'DOWNLOAD_DELAY': 0.5
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url + '?Nao=0',
                callback=self.parse,
                dont_filter=True,
                meta={'url': url}
            )

    def parse(self, response):
        count = int(re.findall(re.compile(r'numberOfResults":"(.*?)"', re.S), response.text)[0])
        page = count // 24
        if page == 0:
            yield scrapy.Request(
                url=response.url,
                callback=self.parse_product,
                dont_filter=True,
                meta={'url': response.url}
            )
        else:
            for x in range(page + 1):
                url = str(response.url).replace('?Nao=0', f'?Nao={x*24}')
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_product,
                    dont_filter=True,
                    meta={'url': url}
                )
                break

    def parse_product(self, response):
        json_data = json.loads(str(
            re.findall(re.compile(r'digitalData.content=(.*?)thdAnalyticsEvent=', re.S), response.text)[
                0]).strip().strip(';'))
        for data in json_data['product']:
            avail = data['productInfo']['availabilityStatus']['shipping']['sth']
            productid = data['productInfo']['sku']
            if avail == 'available':
                detail_url = f'https://www.homedepot.com/p/svcs/frontEndModel/{productid}?_={str(int(time.time()) * 1000)}'
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_detail,
                    dont_filter=True,
                    meta={'url': response.meta.get('url')}
                )

    def parse_detail(self, response):
        datas = json.loads(response.text)
        item = {}
        item['origin_url'] = response.meta.get('url')
        # 产品唯一id
        item['product_id'] = datas['primaryItemData']['partNumber']
        # 产品详情地址
        item['product_url'] = f"https:{datas['primaryItemData']['webUrl']}"
        # 产品原价
        try:
            item['original_price'] = datas['primaryItemData']['itemExtension']['pricing']['originalPrice']
        except Exception:
            item['original_price'] = ''
        # 产品现价
        try:
            item['current_price'] = datas['primaryItemData']['itemExtension']['pricing']['specialPrice']
        except Exception:
            item['current_price'] = ''
        # 品牌
        try:
            item['brand'] = datas['primaryItemData']['info']['brandName']
        except Exception:
            item['brand'] = ''
        # model号
        item['model'] = datas['primaryItemData']['info']['modelNumber']
        # 产品描述
        item['description'] = datas['primaryItemData']['info']['description']
        # 标题
        item['title'] = datas['primaryItemData']['info']['productLabel']
        try:
            shiptohome = datas['fulfillment']['shipping']['shipToHome']
        except Exception:
            shiptohome = ''
        if shiptohome:
            # 配送费
            ship_price = shiptohome['hasFreeShipping']
            if ship_price is True:
                item['ship_price'] = '0'
            else:
                try:
                    item['ship_price'] = shiptohome['freeShippingThreshhold']
                except Exception:
                    item['ship_price'] = ''
            instock_url = f"https://www.homedepot.com/mcc-cart/v2/info/storefulfillment?itemId={item['product_id']}&keyword=6673"
            yield scrapy.Request(
                url=instock_url,
                callback=self.parse_instock,
                dont_filter=True,
                meta={
                    'item': item
                }
            )

    def parse_instock(self, response):
        item = response.meta.get('item')
        datas = json.loads(response.text)
        item['img_url'] = str(
            datas['storeFulfillment']['storeFulfillmentDetails']['sku']['media']['mediaEntry']['location']).replace(
            '64_65.jpg', '64_1000.jpg')

        try:
            fulfillmentOptions = \
                datas['storeFulfillment']['storeFulfillmentDetails']['primaryStore']['fulfillmentOptions'][
                    'buyOnlinePickupInStore']
        except Exception:
            fulfillmentOptions = ''
        try:
            if fulfillmentOptions:
                item['current_area_dcs'] = fulfillmentOptions['inventory']['expectedQuantityAvailable']
                total_dcs = int(item['current_area_dcs'])
                store_list = datas['storeFulfillment']['storeFulfillmentDetails']['alternateStores']['store']
                a_list = []
                a_dict = {}
                for store in store_list:
                    city = store['address']['city']
                    instock = store['fulfillmentOptions']['buyOnlinePickupInStore']['inventory'][
                        'expectedQuantityAvailable']
                    a_dict[city] = instock
                a_list.append(a_dict)
                for v in a_dict.values():
                    total_dcs += v
                item['total_dcs'] = total_dcs
                item['extra_area_dcs'] = str(a_list)
            else:
                item['total_dcs'] = 0
                item['current_area_dcs'] = ''
                item['extra_area_dcs'] = ''
            print(item)
        except KeyError:
            yield scrapy.Request(
                url=response.url,
                callback=self.parse_instock,
                meta={'item': response.meta.get('item')}
            )


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute(['scrapy', 'crawl', 'demo'])
