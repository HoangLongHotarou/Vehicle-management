import 'dart:io';

import 'package:flutter/material.dart';
import 'package:license_plate_detect/core/theme/app_color.dart';

import '../../../core/models/vehicle.dart';

class InfoVehicleV2 extends StatelessWidget {
  const InfoVehicleV2({
    Key? key,
    required this.vehicles,
    required this.image,
  }) : super(key: key);

  final List<Vehicle> vehicles;

  final File image;

  String SplitTime(String time){
    final splitted = time.split('.');
    return splitted[0];
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            children: [
              vehicles.isNotEmpty ? Text('Kết quả : '+vehicles.length.toString()+' biển số xe',style: Theme.of(context).textTheme.headline6!.copyWith(fontSize: 18),) : Container(),
            ],
          ),
        ),
        SizedBox(
          height: 105 * vehicles.length.toDouble(),
          child: ListView.builder(
              padding: EdgeInsets.all(8),
              itemCount: vehicles.length,
              itemBuilder: (BuildContext context, int index) {
                return Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: AppColor.primarySwatch[50]!,width: 1)),
                  margin: const EdgeInsets.only(bottom: 12),
                  child: Row(
                    children: [
                      Expanded(
                        flex: 1,
                        child: ClipRRect(
                          borderRadius: const BorderRadius.only(topLeft: Radius.circular(12),bottomLeft: Radius.circular(12)),
                          child: Image.file(image,height: 90,fit: BoxFit.fill,),
                        ),
                      ),
                      //SizedBox(width: 12,),
                      Expanded(
                        flex: 2,
                        child: Container(
                          //decoration: BoxDecoration(color: AppColor.white,borderRadius: BorderRadius.circular(20)),
                          padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                          //margin: EdgeInsets.all(12),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Biển số xe : '+ vehicles[index].plate!,style: TextStyle(fontWeight: FontWeight.bold,fontSize: 18),),
                              Text(vehicles[index].username! != 'unknown' ? 'Chủ xe : '+vehicles[index].username! : 'Chủ xe : người lạ'),
                              Text(vehicles[index].turn! == 'in' ? 'Thời gian vào : ' : 'Thời gian ra : '),
                              Text(vehicles[index].information!.date! + ' '+ SplitTime(vehicles[index].information!.time!), )
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                );
              }),
        ),
      ],
    );
  }
}