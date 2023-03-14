// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:license_plate_detect/core/component/app_text_field.dart';
import 'package:license_plate_detect/core/component/build_button.dart';
import 'package:license_plate_detect/core/models/vehicle_info.dart';
import 'package:license_plate_detect/feature/personalinfomation/presention/EditProfilePage.dart';
import 'package:license_plate_detect/feature/personalinfomation/widget/profile_widget.dart';
import 'package:license_plate_detect/feature/personalinfomation/widget/profile_widget_local.dart';
import 'package:license_plate_detect/feature/settings/presention/SettingsPage.dart';
import 'package:license_plate_detect/feature/home/presention/HomePage.dart';
import 'package:license_plate_detect/services/api/app_api.dart';
import 'package:license_plate_detect/ultis/checkInternet/checkInternet.dart';

import '../../../core/models/User.dart';
import '../../../core/theme/app_color.dart';
import '../../../core/theme/app_data.dart';
import '../../../services/localstorage/localStorage.dart';
import '../widget/button_widget.dart';
import '../widget/vehicle_item.dart';

class PersonalInfomationPage extends StatefulWidget {
  const PersonalInfomationPage({super.key});

  @override
  State<PersonalInfomationPage> createState() => _PersonalInfomationPageState();
}

User userLocal = new User();

class _PersonalInfomationPageState extends State<PersonalInfomationPage> {
  int _selectedIndex = 1;

  void _onItemTapped(int index) {
    if (index == 0) {
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) {
        return MyHomePage();
      }));
    }

    if (index == 2) {
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) {
        return SettingsPage();
      }));
    }
    setState(() {
      _selectedIndex = index;
    });
  }

  var isDeviceConnected = false;
  bool isAlertSet = false;

  void checkConnection() async {
    bool checkConnection =
        await checkInternet.getConnectivity(isDeviceConnected, isAlertSet);
    if (!checkConnection) {
      checkInternet.showDialogBox(context, isDeviceConnected, isAlertSet);
      setState(
        () => isAlertSet = true,
      );
    }
  }

  @override
  void initState() {
    // TODO: implement initState
    checkConnection();
    setState((){
      userLocal = LocalStorage.getUser();
    });
    // print('username : '+userLocal.username!);
    // print('email : '+userLocal.email!);
    // print('firstname : '+userLocal.firstName!);
    // print('lastname : '+userLocal.lastName!);
    // print('phonenumber : '+userLocal.phoneNumber!);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    return Scaffold(
      backgroundColor: AppColor.white,
      appBar: AppBar(
        title: Text(
            "Thông tin cá nhân",
            textAlign: TextAlign.start,
            style: Theme.of(context).textTheme.headlineMedium!,
          ),
        backgroundColor: Colors.transparent,
        leadingWidth: 0,
        elevation: 0,
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.home_outlined),
            label: 'Trang chủ',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.info_outline),
            label: 'Thông tin',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.settings),
            label: 'Cài đặt',
          ),
        ],
        currentIndex: _selectedIndex,
        unselectedItemColor: Colors.grey,
        selectedItemColor: AppColor.primaryColor,
        onTap: _onItemTapped,
      ),
      body: SafeArea(
        child: ListView(children: [
          // Row(
          //   mainAxisAlignment: MainAxisAlignment.start,
          //   children: [
          //     Padding(
          //       padding: const EdgeInsets.all(24),
          //       child: Text('Thông tin cá nhân',
          //           style: Theme.of(context).textTheme.headlineMedium!
          //           //.copyWith(color: Colors.white),
          //           ),
          //     ),
          //   ],
          // ),
          // SizedBox(
          //   height: 24,
          // ),
          // Container(
          //   height: size.height *  0.4,
          //   width: size.width,
          //   decoration: BoxDecoration(
          //     borderRadius: BorderRadius.only(bottomLeft: Radius.circular(20),bottomRight: Radius.circular(20)),
          //     color: AppColor.primarySwatch[50]),
          // ),
          Container(
            height: size.height * 0.40,
            //color: Colors.amber,
            margin: EdgeInsets.symmetric(horizontal: 24),
            child: LayoutBuilder(builder: (context, constraints) {
              double innerHeight = constraints.maxHeight;
              double innerWidth = constraints.maxWidth;
              return Stack(
                fit: StackFit.expand,
                children: [
                  Positioned(
                    bottom: 30,
                    left: 0,
                    right: 0,
                    child: Container(
                      height: innerHeight * 0.55,
                      decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(30),
                          boxShadow: const [
                            BoxShadow(
                                color: Colors.grey,
                                blurRadius: 5.0,
                                offset: Offset(0, 5)),
                            // BoxShadow(
                            //   color: Colors.white,
                            //   offset: Offset(-2,0)),
                            // BoxShadow(
                            //   color: Colors.white,
                            //   offset: Offset(-5,0)),
                          ],
                          color: Colors.grey[200]),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          SizedBox(
                            height: 70,
                          ),
                          buildName(userLocal),
                        ],
                      ),
                    ),
                  ),
                  Positioned(
                    top: 0,
                    left: 0,
                    right: 0,
                    child: Center(
                        child: userLocal.avatar != null
                            ? ProfileWidget(
                                imagePath: userLocal.avatar!,
                                onNavigator: (() {
                                  Navigator.push(context,
                                      MaterialPageRoute(builder: (context) {
                                    return EditProfilePage();
                                  }));
                                }),
                                onClicked: () {})
                            : ProfileWidgetLocal(
                                imagePath: "assets/avata_default.jpg",
                                onNavigator: (() {
                                  Navigator.push(context,
                                      MaterialPageRoute(builder: (context) {
                                    return EditProfilePage();
                                  }));
                                }),
                                onClicked: () {})),
                  )
                ],
              );
            }),
          ),
          // SizedBox(
          //   height: 24,
          // ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Danh sách xe đăng ký',
                    style: Theme.of(context).textTheme.headlineSmall!),
                SizedBox(
                  height: 12,
                ),
                FutureBuilder(
                  future: AppAPI.VehicleByUser(),
                  builder: (BuildContext context, AsyncSnapshot snapshot) {
                    if (snapshot.connectionState == ConnectionState.none) {
                      return Center(child: CircularProgressIndicator());
                    } else if (snapshot.connectionState ==
                        ConnectionState.waiting) {
                      return Center(child: CircularProgressIndicator());
                    } else if (snapshot.hasData) {
                      List<VehicleInfo> vehicles = snapshot.data;
                      return vehicles.isNotEmpty
                          ? SizedBox(
                              height: 80 * vehicles.length.toDouble(),
                              child: ListView.builder(
                                itemCount: vehicles.length,
                                itemBuilder: (context, index) {
                                  return VehicleItem(
                                    vehicles: vehicles,
                                    index: index,
                                  );
                                },
                              ))
                          : Text('Tài khoản chưa đăng ký xe',
                              style: Theme.of(context)
                                  .textTheme
                                  .headlineSmall!
                                  .copyWith(
                                      fontSize: 16,
                                      fontWeight: FontWeight.normal));
                    } else if (snapshot.hasError) {
                      return Text('Lỗi : ${snapshot.error}',
                          style: TextStyle(color: Colors.black, fontSize: 20));
                    }
                    return CircularProgressIndicator();
                  },
                )
              ],
            ),
          )
        ]),
      ),
    );
  }

  Widget buildName(User user) => Column(
        mainAxisAlignment: MainAxisAlignment.start,
        //crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            user.username!,
            style: Theme.of(context)
                .textTheme
                .headlineMedium!
                .copyWith(color: AppColor.primaryColor),
          ),
          SizedBox(
            height: 4,
          ),
          Text(
            user.email!,
            style: Theme.of(context)
                .textTheme
                .titleSmall!
                .copyWith(color: Colors.grey),
          ),
          SizedBox(
            height: 4,
          ),
          Text(
            user.phoneNumber!,
            style: Theme.of(context)
                .textTheme
                .titleSmall!
                .copyWith(color: Colors.grey),
          ),
          SizedBox(
            height: 4,
          ),
          if (user.firstName != null && user.lastName != null)
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  user.lastName! + ' ' + user.firstName!,
                  style: Theme.of(context)
                      .textTheme
                      .titleSmall!
                      .copyWith(color: Colors.grey),
                ),
              ],
            )
        ],
      );
}
